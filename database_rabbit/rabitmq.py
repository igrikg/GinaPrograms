import pika
from typing import Callable
import json


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

    def __del__(self):
        self.connection.close()

    def create_queue(self, name_queue: str):
        self.channel.queue_declare(queue=name_queue)
        self.channel.queue_bind(exchange=self.__exchange, queue=name_queue, routing_key=name_queue)

    def start_consuming(self):
        self.channel.start_consuming()

    def get_message(self, name_queue: str) -> dict:
        method_frame, header_frame, body = self.channel.basic_get(name_queue)
        print(method_frame, header_frame, body)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            return {}

    def attach_consumer_callback(self, name_queue: str, func: Callable):
        # ch, method, properties, body
        self.channel.basic_consume(queue=name_queue, on_message_callback=func, auto_ack=True)

    def publish_message(self, name_queue: str, body_message: dict):
        self.channel.basic_publish(self.__exchange, routing_key=name_queue,
                                   body=json.dumps(body_message), mandatory=True)


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

    rc.publish_message('B', {'motor':'slit1','command':'goto', 'position':123})
    print(rc.get_message('B'))
    #rc.start_consuming()
