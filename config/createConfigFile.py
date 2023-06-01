import pickle

config=
{
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
                        'name':'',
                        'unit':'',
                        'converting_coefficient':1.0,
                        'device': '',
                        'use_encoder': False,
                        'use_encoder_aliment': False,
                        'encoder_device':'',
                        'encoder_unit':'',
                        'encoder_converting_coefficient':1.0,
                        'limit_minus':-500,
                        'limit_plus':500,
                        'before_command': ('',''),
                        'after_command': ('','')
                    },

                ]


        }


}
pickle.dump(config, '')