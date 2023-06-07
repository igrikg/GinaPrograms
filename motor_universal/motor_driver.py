import sys


# rabbitMQ, db, run

class MotorsSystem:
    def __init__(self, name: str, config:dict):
        pass
    def run(self):
        pass
    def __make_command(self):
        pass


if __name__ == '__main__':
    from config.configurations import Configuration
    a = Configuration()
    MotorsSystem('MCU-2', a)
