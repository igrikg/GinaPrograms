from comportoperation import SerialDevice

class MotorsSystems:
    def __init__(self, config: dict):
        self.__buzy = False
        self.config = config
        self.serialdevice = SerialDevice(config)
        self.debug = {}

    def move(self, motor_name:str, position: int):
        pass
    def goto(self, motor_name:str, position: int):
        pass
    def set_position(self, motor_name:str, position: int):
        pass
    def goto_home(self, motor_name:str):
        pass
    def goto_minus_limit(self, motor_name:str):
        pass
    def goto_plus_limit(self, motor_name:str):
        pass
    def stop(self, motor_name:str):
        pass




if __name__ == '__main__':
    from config.configurations import Configuration
    a = Configuration()['MCU-2']
    MotorsSystems(a)