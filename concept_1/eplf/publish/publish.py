"""
This script is run inside the EPLF-publish container.

This script retrieves a random number of rows (between 1000 and 10000) from the 'Payments' table of the EPLF database
that have not already been retrieved previously (and are therefore not present in the 'Log' table).

It then checks if the IBAN is valid and writes the data to the 'Log' table in the database.
If the IBAN is invalid, it sets the 'faulty' column to True.

It also publishes the data to the RabbitMQ 'data' queue.

It runs in a loop with a 10 minute delay between each iteration.
"""

import json
import time
import random
import pika
import psycopg2
from schwifty import IBAN
from schwifty.exceptions import InvalidChecksumDigits



# ------------- Database / data functions ------------- #

def connect_to_db(host, dbname, user, password, port=5432):
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password,
            port=port,
        )
        print(f"Successfully connected to PostgreSQL database with id {id(conn)}")
    except Exception as e:
        print(f"Error occurred: {e}")
    return conn


def get_data_from_db(conn):
    # This function retrieves a random number of rows (between 1000 and 10000) from the 'Payments' table in the database
    # that have not already been retrieved previously (and are therefore not in the 'Log' table)
    cursor = conn.cursor()
    num_rows_to_retrieve = random.randint(1000, 10000)
    cursor.execute(f"""
        SELECT id, amount, iban, TO_CHAR(payment_date, 'YYYY-MM-DD')
        FROM Payments
        WHERE id NOT IN (SELECT payment_id FROM Log)
        LIMIT {num_rows_to_retrieve}
    """)
    return cursor.fetchall()


def is_iban_valid(iban):
    # Returns True if the IBAN is valid, False otherwise
    try:
        iban = IBAN(iban)
        return True
    except InvalidChecksumDigits:
        return False


def filter_data_for_invalid_iban(data):
    # This function filters the data for rows with invalid IBANs
    filtered_data = []

    for row in data:
        iban = row[2]

        if is_iban_valid(iban):
            filtered_data.append(row)

    return filtered_data


def write_data_to_db(conn, data):
    # This function writes the data to the 'Log' table in the database
    # It checks beforehand if the IBAN is valid, and if not, it sets the 'faulty' column to True
    fault_count = 0

    cursor = conn.cursor()

    for row in data:

        # Validate the IBAN
        if not is_iban_valid(row[2]):
            fault_count += 1

            payment_id = row[0]
            cursor.execute(
                "INSERT INTO Log (payment_id, iban, validated, inserted, faulty) VALUES (%s, %s, False, now() AT TIME ZONE 'UTC', True)",
                (payment_id, row[2])  # row[2] is iban in the selected data
            )

        else:

            payment_id = row[0]
            cursor.execute(
                "INSERT INTO Log (payment_id, iban, validated, inserted, faulty) VALUES (%s, %s, False, now() AT TIME ZONE 'UTC', False)",
                (payment_id, row[2])  # row[2] is iban in the selected data
            )

    conn.commit()
    print(f"Successfully added {len(data)} rows to the Log table of which {fault_count} had invalid IBANs")



# ------------- Main function ------------- #

def main():
    # Connect to database.
    conn = connect_to_db(host='192.168.0.23', dbname='db', user='postgres', password='postgres')

    # Provide username and pw for mq.
    credentials = pika.PlainCredentials('rabbit', 'rabbit')

    # Here we're creating the connection to RabbitMQ.
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.22', credentials=credentials, heartbeat=10000))
    channel = connection.channel()

    # Declare the queue from which we want to receive messages.
    channel.queue_declare(queue='data')

    sent_counter = 0

    while True:
        # Retrieve data from database.
        data = get_data_from_db(conn)

        # Write the IDs of the data that was published into the 'Log' table in the database.
        write_data_to_db(conn, data)

        filtered_data = filter_data_for_invalid_iban(data)

        # Convert all data to a JSON string and send as a single message
        message = json.dumps(filtered_data)

        # Publish the message to the queue.
        channel.basic_publish(exchange='', routing_key='data', body=message)

        # Increment the counter.
        sent_counter += len(filtered_data)
        print(f"Sent {sent_counter} rows in total\n")

        # Wait 10 minutes before sending the next message.
        time.sleep(600)


if __name__ == '__main__':
    main()
