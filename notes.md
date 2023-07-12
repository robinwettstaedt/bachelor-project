### Things to change:

- EPLF time span to 600 (currently 60, 1 min)

- ZD verarbeitungs variationszeit (fuers debuggen kleiner gemacht)


- EPLF container Dockerfile have all scripts running (CMD [ "python", "-u", "./publish.py" ])
or have 3 separate containers for the 3 things to do






### Doing right now


- fix comments, docstrings, order of functions, spacing, make nice

- try to see if pushing the time i gave the fill_db to fill the db helps the publish.py to get some rows when it first starts (its always 0 now)





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