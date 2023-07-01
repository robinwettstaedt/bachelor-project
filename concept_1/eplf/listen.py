import json
import pika


def callback(ch, method, properties, body):
    # Decode the JSON string back into a Python list
    data = json.loads(body)

    # Now, data is a list of rows, where each row is represented as a list of its column values.
    # You can iterate over these rows and perform actions on them.
    for row in data:
        # Each row is a list of column values. Here you can write the logic for processing each row.
        print(f'Received row: {row}')


def main():
    # Provide username and pw for mq.
    credentials = pika.PlainCredentials('rabbit', 'rabbit')

    # Here we're creating the connection to RabbitMQ.
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.22', credentials=credentials))
    channel = connection.channel()

    # Declare the queue from which we want to receive messages.
    channel.queue_declare(queue='my_queue')

    # Here we tell RabbitMQ that we want to call the 'callback' function defined above
    # when a message is received on 'my_queue'.
    channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)

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