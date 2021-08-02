### flask_mysql 패키지 이용시 : 개발용 -> 설치용은 mysql-connector-python 패키지 이용

### 설치시 변경
# MYSQL_HOST = 'mysql://b55f6c362f76c3:96860c7c@us-cdbr-east-04.cleardb.com/heroku_f92a588680a967f'
#######################################
# MYSQL_HOST = 'localhost'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'charlie-lyc'
# MYSQL_DB = 'flask_mysql'
# MYSQL_CURSORCLASS = 'DictCursor'

##############################################################################
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'flask-app'

SECRET_KEY = 'flask-app'
