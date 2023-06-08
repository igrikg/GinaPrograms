import motor_class_db as tables_db
from config.configurations import Configuration
from pony.orm import db_session,delete


class MotorSystemDataBase():
    def __init__(self, name_systems: str, config:dict) -> None:
        self.__db = tables_db.db
        self.__name_systems = name_systems
        self.__list_of_tables = self.__get_list_of_tables()
        self.__set_right_name_tables()
        self.__db.bind(provider='postgres', user=config['database']['user'], password=config['database']['password'],
                        host=config['database']['ipAddress'], database=config['database']['namedb'])
        self.__db.generate_mapping(create_tables=True)
        self.__clear_tables()
        self.set_position_data_all()



    def __get_list_of_tables(self):
        res = []
        for a in tables_db.__dir__():
            if a[:2] == '__': continue
            if tables_db.__dict__[a].__module__ == tables_db.__name__.split('.')[-1]:
                res.append(self.__db.__dict__[tables_db.__dict__[a].__name__])
        return res


    def __set_right_name_tables(self):
        for table_name in self.__list_of_tables:
            table=self.__db.__dict__[table_name.__name__]
            table._table_ = f'{self.__name_systems}_{table._table_}'

    def __clear_tables(self):
        with db_session:
            for table in self.__list_of_tables:
                delete(p for p in table)

    def set_position_data_all(self):
        with db_session:
            self.__db.PositionTable(motor_name='name', position=20, encoder_position=0)
        with db_session:
            self.__db.PositionTable['name'].position=199




a = Configuration()
a = MotorSystemDataBase('MSU-2', a)

#config = Configuration()
#db.generate_mapping(create_tables=True)