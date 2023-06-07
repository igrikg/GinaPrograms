from comportoperation import SerialDevice
from typing import Tuple, List
import re
POSITION_STR = 'POSITION'
class MotorDriver:

    def __init__(self, config: dict, serial: SerialDevice):
        self.__buzy: bool = False
        self.config: dict = config
        self.serialdevice: SerialDevice = serial
        self.debug: bool = False
        self.current_position: int = 0

    def __check_message(message: Tuple, result: str) -> bool:


        return False



    def __repeat_sending(self, message: Tuple) -> bool:
        res = False
        for _ in self.config['repeat_message']:
            res = self.__check_message(message, self.serialdevice.send_message(message))
            if res: return True
        return res



    def __send_message(self, message: Tuple) -> bool:
        if not self.config['repeat_all_message']:
            pass
        else:
            pass

    def __send_list_of_message(self, messages: List) -> bool:
        res = False
        if self.config['repeat_all_message']:
            res_part = False
            for _ in self.config['repeat_message']:

                for message in messages:
                    res_part = self.__send_message(message)
                    if not res_part: break
        else:

            for message in messages:
                self.__send_message(message)








    def init(self, motor_name: str):
        pass

    def goto(self, motor_name: str, position: int):
        pass

    def set_position(self, motor_name: str, position: int):
        pass

    def get_position(self, motor_name: str)->int:
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
    ss = MotorDriver(a,SerialDevice(a))
    #ss.send_message
