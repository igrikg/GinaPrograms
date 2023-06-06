from comportoperation import SerialDevice

class MotorsSystems:
    def __init__(self, config: dict):
        self.__buzy = False
        self.config = config
        self.serialdevice = SerialDevice(config)
        self.debug = {}

    def move(self, position: int):
        pass
    def goto(self, position: int):
        pass
    def set_position(self, position: int):
        pass
    def goto_home(self):
        pass
    def goto_minus_limit(self):
        pass
    def goto_plus_limit(self):
        pass
    def stop(self):
        pass




if __name__ == '__main__':
    from config.configurations import Configuration
    a = Configuration()['MCU-2']
    MotorsSystems(a)