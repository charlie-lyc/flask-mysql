import mysql.connector
from mysql.connector import errorcode
from database import db

# DB_NAME  = 'flask_mysql'
DB_NAME  = 'heroku_f92a588680a967f'

TABLES = {}
TABLES['users'] = (
    'create table users('
    'id int(11) auto_increment primary key,'
    ' name varchar(100),'
    ' email varchar(100),'
    ' username varchar(100),'
    ' password varchar(100),'
    ' registered_date datetime not null default current_timestamp);'
)
TABLES['articles'] = (
    'create table articles('
    'id int(11) auto_increment primary key,'
    ' title varchar(255),'
    ' author varchar(100),'
    ' body text,'
    ' created_date datetime not null default current_timestamp);'
)


# def create_database():
#     cur = db.cursor()
#     cur.execute('create database if not exists {} default character set utf8;'.format(DB_NAME))
#     print('Database {} created!'.format(DB_NAME))
#     cur.close()

def create_tables():
    cur = db.cursor()
    cur.execute('use {};'.format(DB_NAME))
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print('Creating table {} ... '.format(table_name), end='')
            cur.execute(table_description)
            print('Created!')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Table already exists!')
            else:
                print(err.msg)
    cur.close()