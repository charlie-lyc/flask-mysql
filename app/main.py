from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from passlib.hash import sha256_crypt
# from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect, CSRFError
###########################################################
# from data import Articles
from config import *
from forms import RegisterForm, LoginForm, ArticleForm
from decorators import login_required

###########################################################

app = Flask(__name__)

### Config Secret Key
app.config['SECRET_KEY'] = SECRET_KEY

###########################################################
### flask-mysqldb 이용

### Config MySQL : Reference from https://github.com/alexferl/flask-mysqldb
# app.config['MYSQL_HOST'] = MYSQL_HOST
# app.config['MYSQL_USER'] = MYSQL_USER
# app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
# app.config['MYSQL_DB'] = MYSQL_DB
# app.config['MYSQL_CURSORCLASS'] = MYSQL_CURSORCLASS

### Init MySQL
# mysql = MySQL(app)

###########################################################
### mysql-connector-python 이용

from db_setup import create_tables#, create_database 
from database import db

######### 최초 한번만 실행하고 더 이상 실행되지 않게!!! #############
### 설치 후 커멘트 처리
# create_database()
create_tables()
###########################################################

### Config WTF CSRF : Reference from https://flask-wtf.readthedocs.io/en/0.15.x/csrf/
### WTF_CSRF 를 이용할 경우 앱을 실행하기 전에 app.secret_key 설정이 필요하고 WTF_CSRF_SECRET_KEY 를 별도로 정할 수도 있음 
app.config['WTF_CSRF_ENABLED'] = WTF_CSRF_ENABLED
app.config['WTF_CSRF_SECRET_KEY'] = WTF_CSRF_SECRET_KEY

### Init CSRF Protection
csrf = CSRFProtect(app)

###########################################################

### Fetch Articles from Mockup Data
# Articles = Articles()

######################################################################################################################
######################################################################################################################
@app.route('/')
@app.route('/index')
def index():
    # return 'Hello World!'
    # return '<h1>Hello World!<h1>'
    return render_template('index.html', name='Flask-MySQL App')

@app.route('/home')
def home():
    return render_template('home.html', navbar_home='active')

@app.route('/about')
def about():
    return render_template('about.html', navbar_about='active')

@app.route('/articles')
def articles():
    # cur = mysql.connection.cursor()
    cur = db.cursor()
    # result = cur.execute('select * from articles;')
    ### 인출되는 자료구조가 flask_mysqldb 와는 달리 dict가 아니라 tuple 임  : fetchall -> [(),()...] , fetchone -> (), 
    cur.execute('select * from articles;')
    data = cur.fetchall() # 반복 인출 안됨 그래서 일단 받아 놓음!!!
    # if result > 0:
    if len(data) > 0:
        Articles = reversed(data)
        cur.close()
        return render_template('articles.html', articles=Articles, navbar_articles='active')
    else:
        cur.close()
        flash('No articles found.', 'info')
        return render_template('articles.html', navbar_articles='active')
    ######################################################################
    # return render_template('articles.html', articles=Articles, navbar_articles='active')

### Path Variable : <variable_name> 
@app.route('/articles/<id>')
def article(id):
    # for art in Articles:
    #     ### Only Bracket Notation in dict type!!!
    #     ### Convert Type!!!
    #     if art['id'] == int(id): 
    #         found_article = art
    ######################################################################
    # cur = mysql.connection.cursor()
    cur = db.cursor()
    cur.execute('select * from articles where id=%s', [id])
    found_article = cur.fetchone()
    cur.close()
    ######################################################################
    return render_template('article.html', article=found_article)

### Reference : https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/?highlight=render_field
@app.route('/register', methods = ['GET', 'POST'])
def register():
    register_form = RegisterForm(request.form)
    if request.method == 'POST' and register_form.validate():
        name = register_form.name.data # RegisterForm 클래스를 이용할 경우 '''inst.attr.data''' 를 통해 접근
        email = register_form.email.data
        username = register_form.username.data
        password = sha256_crypt.hash(str(register_form.password.data))
        ### Create and Use DB Cursor
        # 1. cur.execute()를 이용시 f'{}'는 허용되지 않음
        # 2. cur.execute()를 이용시 MySQL shell에서 허용되는 것처럼 소문자 사용 가능
        ###
        ### email 중복 가입 방지 : 로그인시 이용
        # cur = mysql.connection.cursor()
        cur = db.cursor()
        # result_1 = cur.execute('select * from users where email=%s;', [email])
        cur.execute('select * from users where email=%s;', [email])
        # if result_1 > 0:
        if len(cur.fetchall()) > 0:
            ### Flashing message : flash(message, category)
            flash('Your email ALREADY exists.', 'danger') # Flash Message
            return redirect(url_for('login'))
        ### username 중복 가입 방지 : 글 작성시 이용
        # cur = mysql.connection.cursor()
        cur = db.cursor()
        # result_2 = cur.execute('select * from users where username=%s;', [username])
        cur.execute('select * from users where username=%s;', [username])
        # if result_2 > 0:
        if len(cur.fetchall()) > 0:
            ### Flashing message : flash(message, category)
            flash('Your username ALREADY exists.', 'danger') # Flash Message
            return redirect(url_for('register'))
        ### Execute to DB
        # cur = mysql.connection.cursor()
        cur = db.cursor()
        cur.execute('insert into users (name, email, username, password) values (%s, %s, %s, %s);', [name, email, username, password])
        ### Commit to DB
        # mysql.connection.commit()
        db.commit()
        ### Close connection
        cur.close()
        ### Flashing message : flash(message, category)
        flash('You are successfully registered and can log in.', 'success') # Flash Message
        # return redirect('/login') # redirect(location, code, response)
        return redirect(url_for('login')) # url_for(endpoint, **values)
    return render_template('register.html', form=register_form, navbar_register='active')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    ### form.csrf_token 이용을 위해 필요 
    login_form = LoginForm(request.form) 
    if request.method == 'POST':
        email = request.form['email'] # Form 클래스를 이용하지 않을 경우 '''request.form[name]''' 으로도 접근 가능 
        password_candidate = request.form['password']
        # cur = mysql.connection.cursor()
        cur = db.cursor()
        # result = cur.execute('select * from users where email=%s;', [email])
        cur.execute('select * from users where email=%s;', [email])
        data = cur.fetchall()
        # if result > 0:
        if len(data) > 0:
            # password = data['password']
            password = data[0][4] # 데이터 구조가 튜플(row)들의 배열(table) 형태임
            if sha256_crypt.verify(password_candidate, password):
                # app.logger.info('You are successfully logged in!') # Why error...
                ############ Set Session ############# : 다만 세션만으로는 직접 라우트를 타이핑하여 접근하는 것까지 막지는 못함.
                session['logged_in'] = True
                # session['username'] = data['username']
                session['username'] = data[0][3]
                # session['email'] = data['email']
                session['email'] = data[0][2]
                ######################################
                flash('You are now logged in.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Your password NOT mached.', 'warning')
                # msg = 'Your password NOT mached!'
                # return render_template('login.html', form=login_form, navbar_login='active', msg=msg)
        else:
            flash('Your email NOT exists.', 'danger')
            # error = 'Your email NOT exists!'
            # return render_template('login.html', form=login_form, navbar_login='active', error=error)
        cur.close()
    return render_template('login.html', form=login_form, navbar_login='active')

### 세션을 이용해 자연스럽게 로그인/로그아웃 상태로 전환될수 있음
### 하지만 브라우저에 직접 /dashboard 를 타이핑하여 접근하는 것까지 막지는 못함
### 그래서 도입하게 된 것이 Decorator!
# Reference from : https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/

@app.route('/dashboard')
@login_required
def dashboard():
    # cur = mysql.connection.cursor()
    cur = db.cursor()
    # result = cur.execute('select * from articles where author=%s;', [session['username']])
    cur.execute('select * from articles where author=%s;', [session['username']])
    data = cur.fetchall()
    # if result > 0:
    if len(data) > 0:
        Articles = reversed(data)
        cur.close()
        return render_template('dashboard.html', articles=Articles, navbar_dashboard='active')
    else:
        cur.close()
        flash('No articles found.', 'info')
        return render_template('dashboard.html', navbar_dashboard='active')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You are successfully logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    article_form = ArticleForm(request.form)
    if request.method == 'POST' and article_form.validate():
        title = article_form.title.data
        body = article_form.body.data
        # cur = mysql.connection.cursor()
        cur = db.cursor()
        cur.execute('insert into articles (author, title, body) values (%s, %s, %s);', [session['username'], title, body])
        # mysql.connection.commit()
        db.commit()
        cur.close()
        flash('You created new article.', 'success')
        return redirect(url_for('articles'))
    return render_template('add_article.html', form=article_form, navbar_add_article='active')

@app.route('/edit_article/<id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    ### form.csrf_token 이용을 위해 필요 
    edit_form = ArticleForm(request.form)
    # cur = mysql.connection.cursor()
    cur = db.cursor()
    cur.execute('select * from articles where id=%s', [id])
    data = cur.fetchone()
    if request.method == 'POST':
        # if data['author'] == session['username']:
        if data[2] == session['username']:
            title = request.form['title']
            body = request.form['body']
            # cur = mysql.connection.cursor()
            cur = db.cursor()
            cur.execute('update articles set author=%s, title=%s, body=%s where id=%s;', [session['username'], title, body, id])
            # mysql.connection.commit()
            db.commit()
            cur.close()
            flash('You updated the article.', 'success')
            return redirect(url_for('articles'))
        else:
            cur.close()
            flash('Unauthorized Request!', 'danger')
            return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form=edit_form, article=data)

###########################################################

### My Solution
@app.route('/delete_article/<id>')
@login_required
def delete_article(id):
    # cur = mysql.connection.cursor()
    cur = db.cursor()
    cur.execute('select * from articles where id=%s', [id])
    data = cur.fetchone()
    # if data['author'] == session['username']:
    if data[2] == session['username']:
        # cur = mysql.connection.cursor()
        cur = db.cursor()
        cur.execute('delete from articles where id=%s', [id])
        # mysql.connection.commit()
        db.commit()
        cur.close()
        flash('You removed the article.', 'success')
    else:
        flash('Unauthorized Request!', 'danger')
    return redirect(url_for('dashboard'))

### Instructor's Solution : 하지만 form.csrf 적용이 되지 않아서 위의 My Solution으로 대체
# @app.route('/delete_article/<id>', methods=['POST'])
# @login_required
# def delete_article(id):
#     ### form.csrf_token 이용을 위해 필요 
#     delete_form = ArticleForm(request.form)
#     cur = mysql.connection.cursor()
#     cur.execute('delete from articles where id=%s', [id])
#     mysql.connection.commit()
#     cur.close()
#     flash('You removed the article.', 'success')
#     return redirect(url_for('dashboard', form=delete_form))

###########################################################

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

######################################################################################################################
######################################################################################################################
### 설치시 변경
# if __name__ == '__main__':
    # app.debug = True
    # app.run()
    ##################
    # app.run(debug=True) 
