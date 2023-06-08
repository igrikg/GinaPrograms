import sys
from motor_class import MotorDriver
from comportoperation import SerialDevice

# rabbitMQ, db, run

class MotorsSystem:
    def __init__(self, name_of_system: str, config:dict):
        self.__config = config
        self.__serial = SerialDevice(self.__config[name_of_system])
        self.name_of_system = name_of_system
        self.__motors = {}
        self.__add_all_motor()
    def __add_all_motor(self):
        for motor_name in self.__config[self.name_of_system]['motors']:
            self.__motors[motor_name] = MotorDriver(motor_name, self.__config[self.name_of_system], self.__serial)
    def run(self):
        pass
    def __make_command(self):
        pass


if __name__ == '__main__':
    from config.configurations import Configuration
    a = Configuration()
    MotorsSystem('MCU-2', a)
