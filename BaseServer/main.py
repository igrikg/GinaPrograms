from getconfig import get_config
from rabitmq import RabbitMq
import time


class BaseClass:
    def __init__(self, name_server: str = 'B', url: str = 'http://localhost:30000') -> object:
        self.name_server = name_server
        self.config = get_config(url)
        self.__init_queue()

    def __init_queue(self):
        self.__rabit_class = RabbitMq(self.config)
        self.__rabit_class.create_queue(self.name_server)

    def _run_comand(self, *args):
        print('Got a message from Queue B: ', *args, sep='\n')
        time.sleep(2)

    def __run_db(self):
        pass

    def run(self):
        while 1:
            print(time.time())
            self.__rabit_class.get_message_with_feedback(self.name_server, True, lambda x: self._run_comand(x))
            print(time.time())

    def __del__(self):
        print('Server stopped!!!!')


if __name__ == '__main__':
    a = BaseClass()
    a.run()

    #    b._BaseClass__rabit_class.publitsh_message('B', {'motor': 'slit1', 'command': 'goto', 'position': 123})
