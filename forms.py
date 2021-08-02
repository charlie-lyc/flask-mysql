from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, validators

class RegisterForm(FlaskForm):
    name = StringField('Name', [
        validators.DataRequired(), 
        validators.Length(min=3, max=100) 
    ])
    email = StringField('Email', [
        validators.DataRequired(), 
        validators.Length(min=5, max=100) 
    ])
    username = StringField('Username', [
        validators.DataRequired(), 
        validators.Length(min=3, max=100) 
    ])
    password = StringField('Password', [
        validators.DataRequired(),
        validators.Length(min=5, max=100)
    ])
    confirm = PasswordField('Confirm password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Confirmation NOT matched to password')
    ])

class LoginForm(FlaskForm):
    email = StringField('Email', [
        validators.DataRequired(), 
        validators.Length(min=5, max=100) 
    ])
    password = StringField('Password', [
        validators.DataRequired(),
        validators.Length(min=5, max=100)
    ])

class ArticleForm(FlaskForm):
    title = StringField('Title', [
        validators.DataRequired(), 
        validators.Length(min=3, max=255) 
    ])
    body = TextAreaField('Body', [
        # validators.DataRequired(), # <textarea> 에서 required 속성이 POST 메서드 실행시 에러를 발생시킴 !!!
        validators.Length(min=10) 
    ])
    