import pika
import uuid
from typing import Callable, Any, Union
import json


class RabbitMq:
    def __init__(self, config: dict):
        config = config['database']
        credentials = pika.PlainCredentials(config['user'], config['password'])
        connection_parameters = pika.ConnectionParameters(host=config['ipAddress'], port=config['port'],
                                                          credentials=credentials)
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()
        self.__exchange = config['exchange']
        self.channel.exchange_declare(self.__exchange, durable=True, exchange_type='topic')

        self.__response = None
        self.__corr_id = None

    def __del__(self):
        self.connection.close()

    def create_queue(self, name_queue: str):
        result = self.channel.queue_declare(queue=name_queue)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.queue_bind(exchange=self.__exchange, queue=name_queue, routing_key=name_queue)

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

    def get_message_with_feedback(self, name_queue: str, response: Any, func: Callable) -> Any:
        method_frame, header_frame, body = self.channel.basic_get(name_queue)
        if method_frame:
            result = func(json.loads(body))
            if header_frame.reply_to:
                self.channel.basic_publish(
                    self.__exchange,
                    routing_key=header_frame.reply_to,
                    properties=pika.BasicProperties(correlation_id=header_frame.correlation_id),
                    body=json.dumps(response)
                )
            self.channel.basic_ack(method_frame.delivery_tag)
            return result
        else:
            return None

    def __publish_message_with_answer(self, name_queue: str, body_message: dict) -> None:
        self.__response = None
        self.__corr_id = str(uuid.uuid4())
        response_queue = f'{name_queue}_response'
        self.create_queue(response_queue)
        self.channel.basic_consume(
            queue=response_queue,
            on_message_callback=self.__on_response,
            auto_ack=True
        )
        self.publish_message(name_queue=name_queue,
                             body_message=body_message,
                             properties=pika.BasicProperties(
                                 reply_to=response_queue,
                                 correlation_id=self.__corr_id
                             )
                             )

    def publish_message_with_answer_with_waiting(self, name_queue: str, body_message: dict) -> Any:
        self.__publish_message_with_answer(name_queue, body_message)
        self.connection.process_data_events(time_limit=None)
        return self.__response

    def publish_message_with_answer_without_waiting(self, name_queue: str, body_message: dict) -> None:
        self.__publish_message_with_answer(name_queue, body_message)

    def attach_consumer_callback(self, name_queue: str, func: Callable):
        # ch, method, properties, body
        self.channel.basic_consume(queue=name_queue, on_message_callback=func, auto_ack=True)

    def publish_message(self, name_queue: str, body_message: dict,
                        properties: Union[pika.BasicProperties, None] = None) -> None:
        self.channel.basic_publish(self.__exchange, routing_key=name_queue,
                                   body=json.dumps(body_message),
                                   properties=properties, mandatory=True)


if __name__ == '__main__':
    from config.configurations import Configuration
    import time
    print(Configuration)


    def callbackFunctionForQueueB(*args):
        print('Got a message from Queue B: ', *args, sep='\n')
        time.sleep(2)


    def callbackFunctionForQueueB2(*args):
        print('Got a message from Queue B2: ', sep='\n')
        print(args[-1].decode(), sep='\n')


    a = Configuration()
    rc1 = RabbitMq(a)
    rc2 = RabbitMq(a)
    rc1.create_queue('B')
    rc2.create_queue('B')

    rc1.publish_message('B', {'motor': 'slit1', 'command': 'goto', 'position': 123})
    time.sleep(1)
    print(rc2.get_message('B'))
    print("--------------------------------------------")
    rc1.publish_message_with_answer_without_waiting('B', {'motor': 'slit1', 'command': 'goto', 'position': 123})
    time.sleep(1)
    rc2.get_message_with_feedback('B', True, callbackFunctionForQueueB)

    # print("--------------------------------------------")
    # rc1.publish_message('B', {'motor': 'slit1', 'command': 'goto', 'position': 123})
    # time.sleep(1)
    # print(rc2.get_message('B'))
    # rc.start_consuming()
