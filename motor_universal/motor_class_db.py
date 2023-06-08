from pony.orm import Database,Required,PrimaryKey

db = Database()
class PositionTable(db.Entity):
    _table_ = 'positions'
    motor_name = PrimaryKey(str)
    position = Required(int)
    encoder_position = Required(int)
class ParametersTable(db.Entity):
    _table_ = 'parameters'
    id = PrimaryKey(int, auto=True)
    motor_name = Required(str, unique=True)
    parameter_name = Required(str)
    value = Required(str)


db2 = Database()
db_structures = {
      'PositionTable':{ '_table_': 'positions',
                        'motor_name': PrimaryKey(str),
                        'position': Required(int),
                        'encoder_position': Required(int)},

      'ParametersTable':{'_table_':'parameters',
    'id': PrimaryKey(int, auto=True),
    'motor_name': Required(str, unique=True),
    'parameter_name': Required(str),
    'value': Required(str)}
    }

a=[type(class_name, (db2.Entity,), attr) for class_name, attr in db_structures.items()]
print(a)