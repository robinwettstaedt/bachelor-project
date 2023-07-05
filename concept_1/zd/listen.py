import json
import time
import random
from datetime import datetime
import pika
import psycopg2
import psycopg2.errors


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


def insert_into_db(conn, data):
    successfully_inserted_data = []

    # Create a database cursor
    cursor = conn.cursor()

    # will return a value between 0.01 and 0.1 (10ms to 100ms) 95% of the time, and will return 1 (1 second) 5% of the time.
    def generate_sleep_time():
        return random.choices(
            population=[random.uniform(0.01, 0.1), 1],  # The possible sleep times
            weights=[0.95, 0.05],  # The probabilities for each sleep time
            k=1
        )[0]

    # Check if data is list or single record
    if isinstance(data, list):
        # Loop through each record in list
        for item in data:
            try:
                # delay for a random duration
                # time.sleep(generate_sleep_time())

                # Insert the record into database
                cursor.execute("INSERT INTO Payments (id, amount, payment_date) VALUES (%s, %s, %s)", (item[0], item[1], item[2]))
                conn.commit()

                # Add the record to the list of successfully inserted records
                successfully_inserted_data.append(item)

                print(f"Inserted data: {item}")
            except psycopg2.errors.UniqueViolation:
                # Duplicate entry / idempotency
                conn.rollback()
                print(f"Duplicate entry: {item}")

    else:
        # Insert single record into database
        try:
            # delay for a random duration
            # time.sleep(generate_sleep_time())

            cursor.execute("INSERT INTO Payments (id, amount, payment_date) VALUES (%s, %s, %s)", (data[0], data[1], data[2]))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            # Ignore duplicate entry
            conn.rollback()


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
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.22', credentials=credentials, heartbeat=1000))
    channel = connection.channel()

    # Declare the queue.
    channel.queue_declare(queue='data_queue')

    # Set 'on_receive_message' as the callback function for received messages.
    channel.basic_consume(queue='data_queue', on_message_callback=on_receive_message, auto_ack=False)

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