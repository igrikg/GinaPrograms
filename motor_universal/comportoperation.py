from typing import Tuple
from utils import repeat_decorator
import serial
import fakeSerial.fakeSerial as serial


class SerialDevice:
    """
    Work with Com port devices
    """

    def __init__(self, config: dict):
        self.__port = serial.Serial()
        self.__repeat_separately = not config['repeat_all_message']
        self.__send_in_bytes = config['send_in_bytes']
        self.__repeat_message = config['repeat_message']
        self.__port.port = config['port']
        self.__port.baudrate = config['baudrate']

        self.__port.bytesize = config['bytesize']
        self.__port.parity = config['parity']
        self.__port.stopbits = config['stopbits']

        self.__port.xonxoff = config['xonxoff']
        self.__port.rtscts = config['rtscts']
        self.__port.dsrdtr = config['dsrdtr']

    def __write(self, message: str) -> None:
        with self.__port as port:
            port.write(message.encode() if self.__send_in_bytes else message)

    def __read(self, symbol='\n') -> str:
        result = ''
        print('-------------------------')
        with self.__port as port:
            result = port.read_until(symbol).decode() if self.__send_in_bytes else port.read_until(symbol)
        return result

    def send_message(self, message: Tuple) -> bool:
        """

        :param message:
        :return:
        """
        self.__write(message[0])
        if message[1]:
            # self.__repeat_separately
            return repeat_decorator(self.__repeat_message)(lambda x: self.__read(message[0][-1]) == x)(message[1])
        return True


if __name__ == '__main__':
    from config.configurations import Configuration

    a = Configuration()['MCU-2']
    a = SerialDevice(a)
    print(a.send_message(('#02i-1000\n', '#02i-1000\n')))
