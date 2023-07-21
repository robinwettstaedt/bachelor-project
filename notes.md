### Things to change:

multiple eplf-publish containers result in more data per 10 minutes sent to the zd, therefore no good
multiple zds are ok

necesary for the MQ to have the feature to only deliver a message to one subscriber at a time



### TODO:


Both:
- Comments, Code structure, file doc strings


---


### Timings

C2:
- eplf publish.py (10 min)
- eplf republish.py (2 min)
- validator listen.py (30 secs)
- validator publish.py (1 min)
- zd listen.py (5-25ms: 95%, 50ms: 5%)
- interface: 1 min


C1:
- eplf publish.py (10 min)
- eplf republish.py (1 min, 2 min old)
- zd listen.py (5-25ms: 95%, 50ms: 5%)
- interface: 1 min





---


### Ablauf Concept_1

MQ startet

EPLF DB startet (Payments Table, Log Table)

ZD DB startet (Payments Table)

EPLF DB wird gefuellt durch einen short lived container fill_db.py


EPLF publish.py:
- alle 10 min werden 1000-10000 Reihen aus der 'Payments' Tabelle der EPLF DB, die noch nicht in der 'Log' Tabelle sind, herausgeholt
- die Daten werden in die 'Log' Tabelle eingetragen
- die Daten werden an den `data` Kanal der MQ geschickt


ZD listen.py:
- die Nachricht wird aus dem `data` Kanal der MQ entnommen
- jedes Datum wird auf die Validitaet seiner IBAN geprueft

- wenn IBAN valide: eingefuegt in die Payments Tabelle
- Daten mit valider und invalider IBAN werden separat gespeichert und in verschiedenen Messages an den `validation` Kanal der MQ gesendet


EPLF listen.py:
- entnimmt die Nachricht aus dem `validation` Kanal der MQ
- iteriert durch die Daten in der Nachricht
- Je nachdem ob die Nachricht als successful_insertion oder invalid_iban gekennzeichnet ist:
	- updaten der zugehoerigen Reihe in der `Log` Tabelle der EPLF DB mit faulty=True/False und validated=True


EPLF republish.py:
- jede Minute werden aus der `Log` Tabelle der EPLF DB alle Reihen geholt, die unvalidiert (validated=False) sind und eine scheinbar valide IBAN haben (faulty=False)
- um die Menge an zu frueh erneut gesendeten Daten zu verringern, werden die Reihen mithilfe ihres `inserted` Feldes auf ihr Alter gecheckt
- fuer alle Reihen aelter als 2 Minuten wird die zugehoerige Reihe aus der `Payments` Tabelle der EPLF DB geholt und erneut an den `data` Kanal der MQ geschickt


ZD listen.py:
- genauso wie zuvor


Das System ist konsistent wenn alle nachfolgenden Bedingungen stimmen:
1. zd payments == (eplf log all - eplf log faulty=True)

2. zd payments == eplf log validated


Daten mit invalider IBAN wurden im ZD erkannt und koennen ueber das Feld `faulty` in der `Log` Tabelle der EPLF DB eingesehen werden.

Jedes Mal wenn die Verarbeitung einer Nachricht abgeschlossen ist, wird der Erhalt dieser mit einem `Acknowledgement` an die MQ bestaetigt.



---



### Concept 2

MQ startet

EPLF DB startet (Payments Table, Log Table)

ZD DB startet (Payments Table)

EPLF DB wird gefuellt durch einen short lived container fill_db.py


EPLF publish.py:
- alle 10 min werden 1000-10000 Reihen aus der 'Payments' Tabelle der EPLF DB, die noch nicht in der 'Log' Tabelle sind, herausgeholt
- die Daten werden in die 'Log' Tabelle eingetragen
- die Daten werden an den `data` Kanal der MQ geschickt



ZD listen.py:
- die Nachricht wird aus dem `data` Kanal der MQ entnommen
- jedes Datum wird auf die Validitaet seiner IBAN geprueft

- wenn IBAN valide: eingefuegt in die Payments Tabelle
- Daten mit valider und invalider IBAN werden separat gespeichert und je nach Status in die `Log` oder `InvalidLog` Tabelle der ZD DB geschrieben


Validator publish.py:
- Jede 1 Minute wird eine leere Nachricht an die `validator-to-eplf` und `validator-to-zd` Kanäle der MQ gesendet


EPLF validation.py (leere Nachricht empfangen):
- die Nachricht wird aus dem `validator-to-eplf` Kanal der MQ entnommen
- leere Nachricht:
	- Alle unvalidierten Reihen (`validated=False`) werden aus der `Log` Tabelle der EPLF DB geholt
	- Daten werden an den `eplf-to-validator` Kanal der MQ geschickt


ZD validation.py (leere Nachricht empfangen):
- die Nachricht wird aus dem `validator-to-zd` Kanal der MQ entnommen
- leere Nachricht:
	- Alle unvalidierten Reihen (`validated=False`) werden aus der `Log` Tabelle der ZD DB geholt
	- Daten werden an den `zd-to-validator` Kanal der MQ geschickt


Validator listen.py
- die Nachrichten werden aus den `validator-to-eplf` und `validator-to-zd` Kanälen der MQ entnommen
- die in den Nachrichten enthaltenen Reihen werden gegeneinander verglichen
- sind die Reihen gleich, sind sie sowohl in der EPLF, als auch in dem ZD vorhanden und wurden validiert
- Gleiche Reihen werden daher gesammelt und an die `validator-to-eplf` und `validator-to-zd` Kanäle gesendet


EPLF validation.py (Nachricht mit Inhalt empfangen):
- die Nachricht wird aus dem `validator-to-eplf` Kanal der MQ entnommen
- fuer jede Reihe in der erhaltenen Nachricht wird die zugehoerige Reihe in der `Log` Tabelle der EPLF DB mit `validated=True` geupdated


ZD validation.py (Nachricht mit Inhalt empfangen):
- die Nachricht wird aus dem `validator-to-zd` Kanal der MQ entnommen
- fuer jede Reihe in der erhaltenen Nachricht wird die zugehoerige Reihe in der `Log` Tabelle der ZD DB mit `validated=True` geupdated


Das System ist konsistent wenn alle nachfolgenden Bedingungen stimmen:
1. zd log all + invalid log all == eplf log all
(Die Menge der Daten in der `Log` Tabelle der EPLF entspricht der Menge der Daten in den kombinierten `Log` und `InvalidLog` Tabellen der ZD DB)

2. zd payment == eplf log validated == zd log validated
(Die Menge an Daten ist gleich in:
- `Payments` Tabelle der ZD DB
- `Log` Tabelle der EPLF DB (nur validated=True)
- `Log` Tabelle der ZD DB (nur validated=True)
)

Daten mit invalider IBAN wurden im ZD erkannt und koennen in der `InvalidLog` Tabelle der EPLF DB eingesehen werden.

Jedes Mal wenn die Verarbeitung einer Nachricht abgeschlossen ist, wird der Erhalt dieser mit einem `Acknowledgement` an die MQ bestaetigt.

