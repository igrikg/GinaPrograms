import pika
import uuid
from typing import Callable,Any
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
        self.__callback_queue = None
        self.__response = None
        self.__corr_id = None

    def __del__(self):
        self.connection.close()

    def create_queue(self, name_queue: str):
        result = self.channel.queue_declare(queue=name_queue)
        self.channel.queue_bind(exchange=self.__exchange, queue=name_queue, routing_key=name_queue)
        self.__callback_queue = result.method.queue
        self.channel.basic_consume( queue=self.__callback_queue, on_message_callback=self.__on_response, auto_ack=True)

    def __on_response(self, ch, method, props, body):
        if self.__corr_id == props.correlation_id:
            self.__response = body


    def start_consuming(self):
        self.channel.start_consuming()

    def get_message(self, name_queue: str) -> dict:
        method_frame, header_frame, body = self.channel.basic_get(name_queue)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            return {}

    # not release
    def get_message_pith_feetback(self, name_queue: str, func: Callable, response:Any) -> dict:
        method_frame, header_frame, body = self.channel.basic_get(name_queue)
        if method_frame:

            self.channel.basic_publish(self.__exchange,
                          routing_key=header_frame.reply_to,
                          properties=pika.BasicProperties(correlation_id=header_frame.correlation_id),
                          body=json.dumps(response)
                        )
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            return {}



    def publish_message_with_answer(self, name_queue: str, body_message: dict) -> Any:
        self.__response = None
        self.__corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            self.__exchange,
            routing_key=name_queue,
            properties=pika.BasicProperties(
                reply_to=self.__callback_queue,
                correlation_id=self.__corr_id,
                mandatory=True
            ),
            body=json.dumps(body_message),
        )
        self.connection.process_data_events(time_limit=None)
        return self.__response


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
