import serial

class SerialDevice():
    def __init__(self, config: dict):

        self.__port = serial.Serial()
        self.__port.port = config['port']
        self.__port.baudrate = config['baudrate']
        PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
        STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
        FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)

        'bytesize': 8,
        'parity': 'NONE',
        'stopbits': 1,
        'xonxoff': False,
        'rtscts': False,
        'dsrdtr': False,



a = serial.Serial()

__init__(port=None,
         baudrate=9600,
         bytesize=EIGHTBITS,
         parity=PARITY_NONE,
         stopbits=STOPBITS_ONE,
         timeout=None,
         xonxoff=False,
         rtscts=False,
         write_timeout=None,
         dsrdtr=False,
         inter_byte_timeout=None,
         exclusive=None)




if __name__ == '__main__':
    from config.configurations import Configuration
    a = Configuration()['MCU-2']
    print(a)
