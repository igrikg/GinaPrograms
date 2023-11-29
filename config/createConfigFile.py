import json

config = {
    'database':
        {
            'ipAddress': '127.0.0.1',
            'port': 27017,
            'user': 'gina',
            'password': 'gina19',
            'namedb': 'ginadb'
        },
    'database2':
        {
            'ipAddress': '127.0.0.1',
            'port': 5432,
            'user': 'gina',
            'password': 'gina19',
            'namedb': 'ginadb'
        },
    'queue':
        {
            'ipAddress': '127.0.0.1',
            'port': 5672,
            'user': 'gina',
            'password': 'gina19',
            'exchange': 'gina'
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
            'repeat_message': 5,
            'repeat_all_message': True,
            'send_in_bytes': False,
            'port': '/dev/ttyS4',
            'baudrate': 9600,
            'bytesize': 8,  # (5, 6, 7, 8)
            'parity': 'N',  # PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
            'stopbits': 1,  # (1, 1.5, 2)
            'xonxoff': False,
            'rtscts': False,
            'dsrdtr': False,
            'motors': {
                'name': {
                        'ADR' : '01',
                        'RATE' : '100',
                        'TRUE' : 'hhh'
                        },

            },
            'commands': {
                # All of using commands
                # variables from motor like {ADR}, also you should use POSITION
                # name of command : [write command, read command]
                'com1': ['', ''],
                'com2': ['#{ADR}INIT\n', '#{ADR}INIT\n'],
                'com3': ['#{ADR}{RATE}INIT\n', '#{ADR}{RATE}INIT\n'],
                'com4': ['#{ADR}{RATE}INIT\n', '#{ADR}POSITIONINIT\n'],


            },
            # list of commands for current function
            'init': ['com1','com2','com3','com4',],
            'goto': [],
            'get_position': [],
            'set_position': [],
            'get_position_encoder': [],
            'set_position_encoder': [],
            'goto_home': [],
            'goto_minus_limit': [],
            'goto_plus_limit': [],
            'stop': []
        }

}
with open('config.conf', 'w') as f:
    json.dump(config, f)
