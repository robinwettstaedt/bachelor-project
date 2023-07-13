"""
This script is run inside the validator-publish container.

It periodically sends a message to both (the EPLF and ZD) via the message queue,
which triggers them to send the unvalidated rows in their 'Log' tables back to the validator,
which listens for said messages via its own listen.py script.
"""


import time
import pika



# ------------- Main function ------------- #

def main():
    # Provide authentication for the mq
    credentials = pika.PlainCredentials('rabbit', 'rabbit')

    # Creating the connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.22', credentials=credentials, heartbeat=10000))

    # Create the EPLF channel and queue
    eplf_channel = connection.channel()
    eplf_channel.queue_declare(queue='eplf-validation')

    # Create the ZD channel and queue
    zd_channel = connection.channel()
    zd_channel.queue_declare(queue='zd-validation')

    sent_counter = 0

    while True:
        # No message content needed. The message itself is the trigger.
        message = ""

        # Publish the message to the eplf-validation queue.
        eplf_channel.basic_publish(exchange='', routing_key='data', body=message)

        # Publish the message to the zd-validation queue.
        zd_channel.basic_publish(exchange='', routing_key='data', body=message)

        # Increment the counter.
        sent_counter += 1

        print(f"Sent message to both EPLF and ZD.")
        print(f"This is iteration number: {sent_counter}.\n")

        # Wait 10 minutes before sending the next message.
        time.sleep(600)


if __name__ == '__main__':
    main()