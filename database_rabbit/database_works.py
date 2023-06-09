from config.configurations import Configuration
from pony.orm import Database as PonyDatabase, db_session, delete
from typing import Union


class DataBase:
    def __init__(self, name_systems: str, table_config: dict, config: dict) -> None:
        self.__db = PonyDatabase()
        self.__name_systems = name_systems
        self.__list_classes_of_tables = [type(class_name, (self.__db.Entity,), attr)
                                         for class_name, attr in table_config.items()]

        self.__dict_of_tables = {key: self.__db.__getattribute__(key) for key in table_config.keys()}
        self.__set_right_name_tables()

        self.__db.bind(provider='postgres', user=config['database']['user'], password=config['database']['password'],
                       host=config['database']['ipAddress'], database=config['database']['namedb'])
        self.__db.generate_mapping(create_tables=True)
        self.__clear_tables()

    def __set_right_name_tables(self) -> None:
        for table in self.__dict_of_tables.values():
            table._table_ = f'{self.__name_systems}_{table._table_}'

    def __clear_tables(self) -> None:
        with db_session:
            for table in self.__dict_of_tables.values():
                delete(p for p in table)

    def set_new_data_line(self, key_table: str, parameter: dict) -> None:
        """
        Send new line in table name 'key_table'
        :param key_table: name of table
        :param parameter: {column1_name = value, column2_name = value, column3_name = value}
        :return: None
        """
        with db_session:
            self.__dict_of_tables[key_table](**parameter)

    def update_data_line(self, key_table: str, primary_key: Union[int, str], parameter: dict) -> None:
        """
        Update values from 'parameters' in line with 'primary_key' of table name 'key_table'
        :param key_table: name of table
        :param primary_key: primary key of line which should update (int|str)
        :param parameter: {column1_name = value, column2_name = value, column3_name = value}
        :return: None
        """
        with db_session:
            line_class = self.__dict_of_tables[key_table][primary_key]
            for column_name, value in parameter.items():
                key = line_class.__setattr__(column_name, value)







if __name__ == '__main__':
    from motor_universal.motor_class_db import db_structures
    a = Configuration()
    a = DataBase('MSU-2', db_structures, a)

    parameters = {'motor_name': 'theta',
                      'position': 0,
                      'encoder_position': 0,
                      'debug': True
                      }
    a.set_new_data_line('PositionTable', parameters)
    parameters = {'position': 5000,
                  'encoder_position': 0,
                  'debug': False
                  }
    a.update_data_line('PositionTable', 'theta', parameters)


