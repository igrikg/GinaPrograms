import pickle

config = {
    'database':
        {
            'ipAddress':'127.0.0.1',
            'port': 5432,
            'user': 'gina',
            'password': 'gina19',
            'namedb': 'ginadb'
        },
    'queue':
        {
            'ipAddress':'127.0.0.1',
            'port': 5672,
            'user': 'gina',
            'password': 'gina19',
        },
    'motors':
        {
            'motors_settings':
                [
                    {
                        'name': '',
                        'unit': '',
                        'converting_coefficient': 1.0,
                        'device': '',
                        'device_port': 0,
                        'use_encoder': False,
                        'use_encoder_aliment': False,
                        'encoder_device': '',
                        'encoder_device_port': 0,
                        'encoder_unit': '',
                        'encoder_converting_coefficient': 1.0,
                        'limit_minus': -500,
                        'limit_plus': 500,
                        'before_command': ('', ''),
                        'after_command': ('', '')
                    },

                ]


        },
    'MCU-2':
        {
            'port': 'COM1',
            'baudrate': 9600,
            'bytesize': 8,#(5, 6, 7, 8)
            'parity': 'N',#PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
            'stopbits': 1,#(1, 1.5, 2)
            'xonxoff': False,
            'rtscts': False,
            'dsrdtr': False,


            'motors':{}


        }


}
with open('config.conf', 'wb') as f:
    pickle.dump(config, f)