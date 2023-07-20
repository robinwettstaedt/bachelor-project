### Things to change:

- try out concept1 with more containers (multiple eplfs)
multiple eplf-publish containers result in more data per 10 minutes sent to the zd, therefore no good
multiple zds are ok


- try out concept2 with more containers?


### TODO:

- Linux testen

Both:
- Comments, Code structure, file doc strings
- Ablauf in notes.md

Concept_1:


Concept_2:
- docker run anpassen wie in concept1



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


### Ablauf

MQ startet

EPLF DB startet

EPLF DB wird gefuellt durch einen short lived container fill_db.py


EPLF publish.py:

- alle 10 min werden 1000-10000 Reihen aus der 'Payments' Tabelle der EPLF DB, die noch nicht in der 'Log' Tabelle sind, herausgeholt
- die Daten werden in die 'Log' Tabelle eingetragen
- die Daten werden an den `data` Kanal der MQ geschickt, um vom ZD (listen.py) empfangen zu werden


ZD listen.py:
- die Nachricht wird aus dem `data` Kanal der MQ entnommen
- jedes Datum wird auf die Validitaet seiner IBAN geprueft

- wenn IBAN korrekt, dann mit faulty=False
- wenn IBAN inkorrekt, dann mit faulty=True
- somit kann sich ein weiterer Service oder Angestellter die "faulty" Buchungen kuemmern


EPLF listen.py:



EPLF republish.py:



### Concept 2

MQ startet

EPLF DB startet

EPLF DB wird gefuellt durch einen short lived container fill_db.py


EPLF publish.py:

- alle 10 min werden 1000-10000 Reihen aus der 'Payments' Tabelle der EPLF DB, die noch nicht in der 'Log' Tabelle sind, herausgeholt
- die Daten werden in die 'Log' Tabelle eingetragen
	- wenn IBAN korrekt, dann mit faulty=False
	- wenn IBAN inkorrekt, dann mit faulty=True
	- somit kann sich ein weiterer Service oder Angestellter die "faulty" Buchungen kuemmern
- die Daten mit korrekten IBANs werden an den `data` Kanal der MQ geschickt, um vom ZD (listen.py) empfangen zu werden



ZD listen.py:

- entnimmt die Nachricht aus dem 'data' Kanal der MQ
- "verarbeitet" die in der Nachricht enthaltenen Daten (mit Chance auf zufaelligen Fehler) und speichert diese in der "Payments" Tabelle der ZD DB
- die erfolgreich gespeicherten Daten werden auch in die "Log" Tabelle der ZD DB gespeichert





Validator :

- fragt periodisch



EPLF republish.py: