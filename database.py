### mysql-connector-python 패키지 이용
import mysql.connector

config = {
    ### 설치시 변경
    # 'host': 'mysql://b55f6c362f76c3:96860c7c@us-cdbr-east-04.cleardb.com/heroku_f92a588680a967f',
    'host': 'us-cdbr-east-04.cleardb.com',
    'user': 'b55f6c362f76c3:96860c7c',
    'password': 'charlie-lyc',
    ##########################
    # 'host': 'localhost',
    # 'user': 'root',
    # 'password': 'charlie-lyc',
    ##########################
    # 'database': 'flask_mysql' # 처음에 포함하지 않았다가, 데이터베이스가 생성된 이후에 포함 : create database if not exists {} default character set utf8;
}

db = mysql.connector.connect(**config)
