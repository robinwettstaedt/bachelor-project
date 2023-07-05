### Things to change:

- EPLF time span to 600 (currently 60, 1 min)

- ZD verarbeitungs variationszeit (fuers debuggen kleiner gemacht)






### Doing right now

- Falsche IDs im Event vom ZD reporten



also figure out if any rows in the validation message are not actually in the Log table -> report

periodically send any dates again that are in the Log table but are not validated and whose timestamp is older than XX minutes (make new script in EPLF)