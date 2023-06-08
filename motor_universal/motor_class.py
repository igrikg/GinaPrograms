from comportoperation import SerialDevice
from typing import Tuple, List


class MotorDriver:
    """
    Class motor: for operating with independent motor
    """

    def __init__(self, motor_name: str, config: dict, serial: SerialDevice) -> None:
        self.motor_name = motor_name
        self.__buzy: bool = False
        self.config: dict = config
        self.serialdevice: SerialDevice = serial
        self.debug: bool = False
        self.__POSITION_STR = 'POSITION'  # position comands
        self.current_position: int = 0
        self.current_position_encoder: int = 0
        self.init()

    def __check_message(self, message: Tuple, result: str) -> Tuple:
        """
        Function check reading values equine to answer (if consist position value it should be int)
        :param message: tuple of write and read(answer) commands
        :param result:  read return
        :return: (read OK:bool, position value)
        """

        if self.__POSITION_STR in message[1]:

            length = len(self.__POSITION_STR)
            start = message[1].rfind(self.__POSITION_STR)
            left, right = message[1][:start], message[1][start + length:]
            if result[:len(left)] != left and result[-len(right):] != right: return False, None
            position = result[len(left):-len(right)]
            try:
                return True, int(position)
            except ValueError:
                return False, None
        else:
            return message[1] == result, 0
        return False, None

    def __send_list_of_message(self, messages: List) -> Tuple:
        """
        Sending list of commands:
                check result and repeat if it is need
        :param messages: tuple of write and read(answer) commands
        :return: (read OK:bool, position value)
        """
        result, res_part = False, (False, None)
        res_position = None

        repeat_all, repeat_message = (self.config['repeat_message'], 1) if self.config['repeat_all_message'] \
            else (1, self.config['repeat_message'])

        for _ in range(repeat_all):
            for message in messages:
                for _ in range(repeat_message):
                    res_part = self.__check_message(message, self.serialdevice.send_message(message))
                    if res_part[0]:
                        if not res_part[1] is None:
                            res_position = res_part[1]
                        break
            result ^= res_part[0]
            if result:
                break
        return result, res_position

    def __create_list_of_command(self, motor_name: str, key_function: str) -> List:
        result = []
        list_of_command = self.config[key_function]
        parameters = self.config['motors'][motor_name]
        # 'commands'
        for command in list_of_command:
            result.append(
                tuple(
                    map(lambda x: x.format(**parameters), self.config['commands'][command])
                )
            )

        return result

    def __run_commands(self, key_function: str, position=None) -> Tuple:
        self.__buzy = True
        commands_list = self.__create_list_of_command(self.motor_name, key_function)
        if not position is None:
            replace_func = lambda x: x.replace(self.__POSITION_STR, str(position))
            use_for_both = lambda x: (replace_func(x[0]), replace_func(x[1]))
            commands_list = list(map(use_for_both, commands_list))
        result = self.__send_list_of_message(commands_list)
        result = (not result[0], result[1])
        self.__buzy = False
        return result

    def init(self) -> None:
        """ Run initialisation of motor"""
        self.debug, _ = self.__run_commands('init')

    def goto(self, position: int) -> None:
        print(self.debug)
        if self.debug:
            self.debug, _ = self.__run_commands('init')
            if not self.debug: return
        self.debug, _ = self.__run_commands('goto', position)

    def set_position(self, position: int) -> None:
        if self.debug:
            self.debug, _ = self.__run_commands('init')
            if not self.debug: return
        self.debug, _ = self.__run_commands('set_position', position)

    def get_position(self) -> None:
        if self.debug:
            self.debug, _ = self.__run_commands('init')
            if not self.debug: return
        self.debug, pos = self.__run_commands('get_position')
        if not self.debug and not pos is None:
            self.current_position = pos

    def goto_home(self) -> None:
        if self.debug:
            self.debug, _ = self.__run_commands('init')
            if not self.debug: return
        self.debug, _ = self.__run_commands('goto_home')

    def goto_minus_limit(self) -> None:
        if self.debug:
            self.debug, _ = self.__run_commands('init')
            if not self.debug: return
        self.debug, _ = self.__run_commands('goto_minus_limit')

    def goto_plus_limit(self) -> None:
        if self.debug:
            self.debug, _ = self.__run_commands('init')
            if not self.debug: return
        self.debug, = self.__run_commands('goto_plus_limit')

    def set_position_encoder(self, position: int) -> None:
        if self.debug:
            self.debug, _ = self.__run_commands('init')
            if not self.debug: return
            self.debug, _ = self.__run_commands('set_position_encoder', position)

    def get_position_encoder(self) -> None:
        if self.debug:
            self.debug, _ = self.__run_commands('init')
            if not self.debug: return
        self.debug, pos = self.__run_commands('get_position_encoder')
        if not self.debug and not pos is None:
            self.current_position_encoder = pos

    def stop(self) -> None:
        if not self.debug:
            self.debug, _ = self.__run_commands('stop')


if __name__ == '__main__':
    from config.configurations import Configuration

    a = Configuration()['MCU-2']
    ss = MotorDriver('name', a, SerialDevice(a))
    # ss.goto(123)

