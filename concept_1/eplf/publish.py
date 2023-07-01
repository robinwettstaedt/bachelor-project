import json
import time
import random
import pika
import psycopg2


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
    cursor.execute(f"""SELECT * FROM Payments
                       WHERE id NOT IN (SELECT payment_id FROM Log)
                       LIMIT {num_rows_to_retrieve}""")
    return cursor.fetchall()


def write_data_to_db(conn, data):
    # This function writes the data to the 'Log' table in the database
    cursor = conn.cursor()

    for row in data:
        payment_id = row[0]
        cursor.execute("INSERT INTO Log VALUES (payment_id) VALUES (%s)", payment_id)

    conn.commit()
    print(f"Successfully wrote {len(data)} rows to database")


def main():
    # Connect to database.
    conn = connect_to_db(host='192.168.0.23', dbname='Payments', user='postgres', password='postgres')

    # Provide username and pw for mq.
    credentials = pika.PlainCredentials('rabbit', 'rabbit')

    # Here we're creating the connection to RabbitMQ.
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.22', credentials=credentials))
    channel = connection.channel()

    # Declare the queue from which we want to receive messages.
    channel.queue_declare(queue='my_queue')

    while True:
        # Retrieve data from database.
        data = get_data_from_db(conn)

        # Convert all data to a JSON string and send as a single message
        message = json.dumps(data)

        # Publish the message to the queue.
        channel.basic_publish(exchange='', routing_key='my_queue', body=message)

        # Write the IDs of the data that was published into the 'Log' table in the database.
        write_data_to_db(conn, data)

        # Wait 10 minutes before sending the next message.
        time.sleep(600)


if __name__ == '__main__':
    main()