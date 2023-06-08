from comportoperation import SerialDevice
from typing import Tuple, List
import re


class MotorDriver:

    def __init__(self, config: dict, serial: SerialDevice):
        self.__buzy: bool = False
        self.config: dict = config
        self.serialdevice: SerialDevice = serial
        self.debug: bool = False
        self.__POSITION_STR = 'POSITION'
        self.current_position: int = 0

    def __check_message(self, message: Tuple, result: str) -> Tuple:
        if self.__POSITION_STR in message[1]:
            length = len(self.__POSITION_STR)
            start = message[1].rfind(self.__POSITION_STR)
            left, right = message[1][:start], message[1][start + length:]
            position = result.lstrip(left).rstrip(right)
            if result[:len(left)] != left and result[-len(right):] != right: return False, None
            try:
                return True, int(position)
            except ValueError:
                return False, None
        else:
            return message[1] == result, 0
        return False, None

    def __send_list_of_message(self, messages: List) -> Tuple:
        result = False
        res_position = None

        repeat_all, repeat_message = (self.config['repeat_message'], 1) if self.config['repeat_all_message'] \
            else (1, self.config['repeat_message'])

        for _ in range(repeat_all):
            for message in messages:
                for _ in range(repeat_message):
                    res_part = self.__check_message(message, self.serialdevice.send_message(message))
                    if res_part[0]:
                        res_position = res_part[1]
                        break
            result ^= res_part[0]
            if result:
                break

        return result, res_position

    def init(self, motor_name: str):
        print(self.__send_list_of_message([('#456pos466', '546'), ('#456125y466\n', '#456POSITION466\n')]))

    def goto(self, motor_name: str, position: int):
        pass

    def set_position(self, motor_name: str, position: int):
        pass

    def get_position(self, motor_name: str) -> int:
        pass

    def goto_home(self, motor_name: str):
        pass

    def goto_minus_limit(self, motor_name: str):
        pass

    def goto_plus_limit(self, motor_name: str):
        pass

    def stop(self, motor_name: str):
        pass


if __name__ == '__main__':
    from config.configurations import Configuration
    a = Configuration()['MCU-2']
    ss = MotorDriver(a, SerialDevice(a))
    ss.init('sadfsd')
