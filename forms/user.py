from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired
from flask_login import current_user


class RegisterForm(FlaskForm):
    telegram_id = StringField('Телеграм ID', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    telegram_id = StringField('Телеграм ID', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RaspForm(FlaskForm):
    create_class = SubmitField('Создать класс')
    add_class = SubmitField('Войти в новый класс')
    redact_teachers = SubmitField('Учителя')
    redact_corpuses = SubmitField('Корпуса')
    redact_auditories = SubmitField('Ауидитории')

class ObjectTableForm(FlaskForm):
    id = TextAreaField()
    name = TextAreaField()
    submit = SubmitField('Войти')



