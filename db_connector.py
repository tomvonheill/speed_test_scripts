import configparser
import sqlalchemy as sqla
def get_db_config(section):
    config = configparser.ConfigParser()
    config.read('/home/thomas/repos/speed_mapper/db_config.ini')
    fields = ['db_name', 'db_type','host', 'username', 'password', 'port']
    final_config = {}
    for field in fields:
        final_config[field]=config[section][field]
    return final_config

def get_engine(configs):
    db_url = f'{configs["db_type"]}://{configs["username"]}:{configs["password"]}@{configs["host"]}:{configs["port"]}/{configs["db_name"]}'
    engine = sqla.create_engine(db_url)
    return engine

def get_sql(filename):
    with open(filename) as sql_file:
        sql = sql_file.read()
    return sql


