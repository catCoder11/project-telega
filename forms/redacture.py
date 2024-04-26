from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField, TextAreaField
from wtforms.validators import DataRequired


class RedactForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()], default="")
    submit = SubmitField('Сохранить')

class RedactAudForm(RedactForm):
    sost = SelectField("Состояние: ")


class ChooseClassForm(FlaskForm):
    klass = SelectField("Текущий класс: ")
    submit = SubmitField('Сохранить')

class RedactRaspForm(FlaskForm):
    auditory = SelectField("Аудитория")
    teacher = SelectField("Преподаватель")
    subject = SelectField("Предмет")
    time = TimeField("Время начала")
    submit = SubmitField('Сохранить')

