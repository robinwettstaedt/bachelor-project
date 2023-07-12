"""
This script is run inside the validator container.

It listens for messages from both the EPLF and ZD via the message queue,
which contain the unvalidated data from their 'Log' tables.

These records then get compared and the matches get sent back to the EPLF and ZD via the message queue,
so they can update the 'validated' field in their 'Log' tables accordingly.
"""


import json
from datetime import datetime
import pika



# ------------- Message Queue functions ------------- #

def on_receive_message(ch, method, properties, body):


# ------------- Main function ------------- #

def main():
    # Provide authentication for the mq
    credentials = pika.PlainCredentials('rabbit', 'rabbit')

    # Creating the connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.22', credentials=credentials, heartbeat=10000))
    channel = connection.channel()

    # Declare the queue from which to receive messages
    channel.queue_declare(queue='validation')

    # Declare the callback function
    channel.basic_consume(queue='validation', on_message_callback=on_receive_message, auto_ack=False)

    print('Waiting for messages. To exit press CTRL+C')

    try:
        # Start the consumer in an infinite loop
        channel.start_consuming()
    except KeyboardInterrupt:
        # CTRL+C breaks the infinite loop and closes the connection
        channel.stop_consuming()
        connection.close()

if __name__ == '__main__':
    main()