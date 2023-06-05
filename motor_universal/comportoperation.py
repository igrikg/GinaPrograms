import serial


class SerialDevice():
    def __init__(self, config: dict):
        self.config = config
        self.__port = serial.Serial()
        self.__port.port = self.config['port']
        self.__port.baudrate = self.config['baudrate']

        self.__port.bytesize = self.config['bytesize']
        self.__port.parity = self.config['parity']
        self.__port.stopbits = self.config['stopbits']

        self.__port.xonxoff = self.config['xonxoff']
        self.__port.rtscts = self.config['rtscts']
        self.__port.dsrdtr = self.config['dsrdtr']

    def __write(self, message: str) -> None:
        with self.__port as port:
            port.write(message.encode())

    def __read(self) -> str:
        with self.__port as port:
            port.write(b'hello')

    def send_message(self):
        pass

if __name__ == '__main__':
    from config.configurations import Configuration

    a = Configuration()['MCU-2']
    print(a)
