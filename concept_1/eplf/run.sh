#!/bin/sh

# Run the first script in the background
python listen.py &

# Run the second script
exec python publish.py
