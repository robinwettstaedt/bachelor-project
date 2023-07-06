import json
import time
import random
from datetime import datetime
import pika
import psycopg2
import psycopg2.errors
from schwifty import IBAN
from schwifty.exceptions import InvalidChecksumDigits


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
        print(f"\nSuccessfully connected to PostgreSQL database with id {id(conn)}")
    except Exception as e:
        print(f"Error occurred: {e}")
    return conn


def is_iban_valid(iban):
    # Returns True if the IBAN is valid, False otherwise
    try:
        iban = IBAN(iban)
        return True
    except InvalidChecksumDigits:
        return False


def insert_into_db(conn, data):
    successfully_inserted_data = []

    # Create a database cursor
    cursor = conn.cursor()

    # will return a value between 0.01 and 0.1 (10ms to 100ms) 95% of the time, and will return 1 (1 second) 5% of the time.
    def generate_sleep_time():
        return random.choices(
            population=[random.uniform(0.01, 0.05), 0.1],  # The possible sleep times
            weights=[0.95, 0.05],  # The probabilities for each sleep time
            k=1
        )[0]

    # Check if data is list or single record
    if isinstance(data, list):
        # Loop through each record in list
        for item in data:

            # Validate the data item
            if len(item) < 4:
                continue

            # Validate the IBAN
            if not is_iban_valid(item[2]):
                continue

            try:
                # delay for a random duration
                time.sleep(generate_sleep_time())

                # Random 0.1% chance to skip insertion (simulating an internal error)
                if random.random() < 0.001:
                    print("Internal error, payment was not correctly processed")
                    continue

                # Insert the record into database
                cursor.execute("INSERT INTO Payments (id, amount, iban, payment_date) VALUES (%s, %s, %s, %s)", (item[0], item[1], item[2], item[3]))
                conn.commit()

                # Add the record to the list of successfully inserted records
                successfully_inserted_data.append(item)

            except psycopg2.errors.UniqueViolation:
                # Duplicate entry / idempotency
                conn.rollback()
                print(f"Duplicate entry: {item}")

    else:
        # Validate the data item
        if len(data) < 4:
            return successfully_inserted_data

        # Validate the IBAN
        if not is_iban_valid(data[2]):
            return successfully_inserted_data

        # Insert single record into database
        try:
            # delay for a random duration
            time.sleep(generate_sleep_time())

            # Random 0.1% chance to skip insertion (simulating an internal error)
            if random.random() < 0.001:
                print("Internal error, payment was not correctly processed")
                return successfully_inserted_data

            cursor.execute("INSERT INTO Payments (id, amount, iban, payment_date) VALUES (%s, %s, %s, %s)", (data[0], data[1], data[2], data[3]))
            conn.commit()

        # Duplicate entry / idempotency
        except psycopg2.errors.UniqueViolation:
            # Ignore duplicate entry
            conn.rollback()

    # Print status
    if isinstance(data, list):
        print(f"Successfully inserted {len(successfully_inserted_data)} out of the {len(data)} records received into the 'Payments' table of the ZD database.")
    else:
        print(f"Successfully inserted the only received record with id {data[0]} into the 'Payments' table of the ZD database.")

    return successfully_inserted_data


def on_receive_message(ch, method, properties, body):
    data = json.loads(body)

    # connect to the DB
    conn = connect_to_db(host='192.168.0.24', dbname='db', user='postgres', password='postgres')

    # insert data into DB
    successfully_inserted_data = insert_into_db(conn, data)

    # convert the successfully inserted data to a JSON string
    message = json.dumps(successfully_inserted_data)

    # Acknowledge message so it can be removed from the queue
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Message acknowledged: {method.delivery_tag}")

    # send the message to the queue
    ch.basic_publish(exchange='', routing_key='validation_queue', body=message)
    print(f"Message sent to the validation queue.")

    # make sure to close the connection when you're done
    conn.close()


def main():
    # Define RabbitMQ credentials.
    credentials = pika.PlainCredentials('rabbit', 'rabbit')

    # Establish RabbitMQ connection.
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.22', credentials=credentials, heartbeat=10000))
    channel = connection.channel()

    # Declare the queue.
    channel.queue_declare(queue='data')

    # Set 'on_receive_message' as the callback function for received messages.
    channel.basic_consume(queue='data', on_message_callback=on_receive_message, auto_ack=False)

    # Print status and await messages.
    print('Awaiting messages. To exit press CTRL+C')

    try:
        # Start consumer in infinite loop.
        channel.start_consuming()
    except KeyboardInterrupt:
        # Handle shutdown signal.
        channel.stop_consuming()
        connection.close()


if __name__ == '__main__':
    main()