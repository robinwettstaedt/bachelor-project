"""
This script is run inside the EPLF-listen container.

It listens for messages on the 'validation' queue and iterates through the data it receives through said queue.

For each record in the message, it updates the corresponding entry in the 'Log' table to have the 'validated' field set to True.
"""


import json
from datetime import datetime
import pika
import psycopg2



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


def update_db(data, cursor):
    # Iterate over the data
    for row in data:
        # Get the payment_id from the row
        payment_id = row[0]

        # Update the validated field in the 'Log' table where the payment_id matches
        cursor.execute(
            "UPDATE Log SET validated = True WHERE payment_id = %s",
            (payment_id,)
        )


    print(f"Updated {len(data)} records in the 'Log' table of the EPLF database to be validated. \n")



# ------------- Message Queue functions ------------- #

def callback(ch, method, properties, body):
    # Decode the JSON string back into a Python list
    data = json.loads(body)

    # Connect to the database
    conn = connect_to_db(host='192.168.0.23', dbname='db', user='postgres', password='postgres')

    # Create a cursor from the connection
    cursor = conn.cursor()

    # Update the Log table in the database
    update_db(data, cursor)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()



# ------------- Main function ------------- #

def main():
    # Provide username and pw for mq.
    credentials = pika.PlainCredentials('rabbit', 'rabbit')

    # Here we're creating the connection to RabbitMQ.
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.22', credentials=credentials, heartbeat=10000))
    channel = connection.channel()

    # Declare the queue from which we want to receive messages.
    channel.queue_declare(queue='validation')

    # Here we tell RabbitMQ that we want to call the 'callback' function defined above
    # when a message is received on 'validation'.
    channel.basic_consume(queue='validation', on_message_callback=callback, auto_ack=False)

    print('Waiting for messages. To exit press CTRL+C')

    try:
        # Here we start the consumer in an infinite loop.
        channel.start_consuming()
    except KeyboardInterrupt:
        # If the user presses CTRL+C, we break the infinite loop and close the connection.
        channel.stop_consuming()
        connection.close()

if __name__ == '__main__':
    main()