import pika
from config.configurations import Configuration
from typing import Callable


class RabbitMq:
    def __init__(self, config: dict):
        config = config['queue']
        credentials = pika.PlainCredentials(config['user'], config['password'])
        connection_parameters = pika.ConnectionParameters(host=config['ipAddress'], port=config['port'],
                                                          credentials=credentials)
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()
        self.__exchange = config['exchange']
        self.channel.exchange_declare(self.__exchange, durable=True, exchange_type='topic')

    def create_queue(self, name_queue: str):
        self.channel.queue_declare(queue=name_queue)
        self.channel.queue_bind(exchange=self.__exchange, queue=name_queue, routing_key=name_queue)

    def start_consuming(self):
        self.channel.start_consuming()

    def attach_consumer_callback(self, name_queue: str, func: Callable):
        # ch, method, properties, body
        self.channel.basic_consume(queue=name_queue, on_message_callback=func, auto_ack=True)

    def publish_message(self, name_queue: str, body_message: str):
        self.channel.basic_publish(self.__exchange, routing_key=name_queue,
                                   body=body_message, mandatory=True)


if __name__ == '__main__':
    from config.configurations import Configuration
    def callbackFunctionForQueueB(*args):
        print('Got a message from Queue B: ', *args, sep='\n')
    def callbackFunctionForQueueB2(*args):
        print('Got a message from Queue B2: ', sep='\n')
        print(args[-1].decode(), sep='\n')

    a = Configuration()
    rc = RabbitMq(a)
    rc.create_queue('A')
    rc.create_queue('B')
    rc.publish_message('B', 'slit1 goto position')
    # rc.attach_consumer_callback('B', callbackFunctionForQueueB)
    rc.attach_consumer_callback('B', callbackFunctionForQueueB2)
    rc.start_consuming()
