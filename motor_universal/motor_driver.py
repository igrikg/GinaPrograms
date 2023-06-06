import sys



if __name__ == '__main__':
    from config.configurations import Configuration
    a = Configuration()['MCU-2']
    SerialDevice(a)
