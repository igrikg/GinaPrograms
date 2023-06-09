from pony.orm import Required, PrimaryKey

# db2 = Database()
db_structures = {
    'PositionTable': {'_table_': 'positions',
                      'motor_name': PrimaryKey(str),
                      'position': Required(int),
                      'encoder_position': Required(int),
                      'debug': Required(bool)
                      },

    'ParametersTable': {'_table_': 'parameters',
                        'id': PrimaryKey(int, auto=True),
                        'motor_name': Required(str, unique=True),
                        'parameter_name': Required(str),
                        'value': Required(str)
                        },
}

db_default_values = {
    'PositionTable': {'motor_name': '',
                      'position': 0,
                      'encoder_position': 0,
                      'debug': False
                      },

    'ParametersTable': {'id': 0,
                        'motor_name': '',
                        'parameter_name': '',
                        'value': ''
                        }
}


