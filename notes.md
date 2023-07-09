### Things to change:

- EPLF time span to 600 (currently 60, 1 min)

- ZD verarbeitungs variationszeit (fuers debuggen kleiner gemacht)


- EPLF container Dockerfile have all scripts running (CMD [ "python", "-u", "./publish.py" ])
or have 3 separate containers for the 3 things to do






### Doing right now


- fix comments, docstrings, order of functions, spacing, make nice

- try to see if pushing the time i gave the fill_db to fill the db helps the publish.py to get some rows when it first starts (its always 0 now)



2023-07-09 13:06:02 Traceback (most recent call last):
2023-07-09 13:06:02   File "/app/./listen.py", line 103, in <module>
2023-07-09 13:06:02     main()
2023-07-09 13:06:02   File "/app/./listen.py", line 96, in main
2023-07-09 13:06:02     channel.start_consuming()
2023-07-09 13:06:02   File "/usr/local/lib/python3.9/site-packages/pika/adapters/blocking_connection.py", line 1865, in start_consuming
2023-07-09 13:06:02     self._process_data_events(time_limit=None)
2023-07-09 13:06:02   File "/usr/local/lib/python3.9/site-packages/pika/adapters/blocking_connection.py", line 2031, in _process_data_events
2023-07-09 13:06:02     raise self._closing_reason  # pylint: disable=E0702
2023-07-09 13:06:02 pika.exceptions.ChannelClosedByBroker: (406, 'PRECONDITION_FAILED - delivery acknowledgement on channel 1 timed out. Timeout value used: 1800000 ms. This timeout value can be configured, see consumers doc guide to learn more')


eplf-listen







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
