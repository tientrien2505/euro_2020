from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length, Email


class LoginForm(FlaskForm):
    email = StringField('Email', [Email('Không đúng cú pháp')])
    password = PasswordField('Mật khẩu', [Length(min=1, max=10, message='kích thước mật khẩu từ 1 đến 10')])
    submit = SubmitField('Đăng nhập')

class RegisterForm(FlaskForm):
    email = StringField('Email', [Email('Không đúng cú pháp')])
    password = PasswordField('Mật khẩu', [Length(min=1, max=10, message='kích thước mật khẩu từ 1 đến 10')])
    re_password = PasswordField('Nhập lại Mật khẩu', [Length(min=1, max=10, message='kích thước mật khẩu từ 1 đến 10')])
    submit = SubmitField('Đăng nhập')
