import pika

def callback(ch, method, properties, body):
    # This is the function that gets called when a message is received.
    # Here you would write the logic for processing the message.
    print(f'Received {body}')


def main():
    # Here we're creating the connection to RabbitMQ.
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.18.0.10'))
    channel = connection.channel()

    # Here we declare the queue from which we want to receive messages.
    # Change 'my_queue' to specify the name of your queue.
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