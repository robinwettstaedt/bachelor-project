### Things to change:

- try out concept1 with more containers (multiple eplfs)


### TODO:

- Anleitung README

- IBAN Validierung im ZD

- (evtl.) Interface ohne direkten DB Zugriff



### Doing right now

- adjust the timings of validaton and stuff to have some time were the data is actually consistent
already adjusted:
	C2:
		- republish.py (2 min)
		- validator listen.py (45 secs)
		- validator publish.py (1 min)
		- zd listen.py (ms reduziert, (0.001, 0.005), 0.05)
		- eplf publish.py (5 min)




#### Interface Cols

EPLF Payments (all)  |  ZD Payments (all)  |  EPLF Log (all)  |   ZD Log (all)  |  EPLF Log (invalid IBAN)  |   EPLF Log (validated, not faulty)  | ZD Log (validated)

Wann consistent?:
	- wenn alle die losgeschickt wurden auch korrekt verarbeitet wurden
	- Count EPLF Log (not faulty) == Count ZD Log    &&     alle non-faulty sind validated



### Ablauf

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