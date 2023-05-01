from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import date
import json


class RegisterForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    password_repeat = PasswordField('Repeat password')
    submit = SubmitField('register')


class RegisterUsers(FlaskForm):
    userNumber = StringField('Количество пользователей для добавления', default=0)
    year = date.today().strftime('%Y')
    defaultMask = 'ucmc' + year + 'ss'
    mask = StringField('Маска', default=defaultMask)
    submit = SubmitField('Создать пользователей')


class VarsCreation(FlaskForm):
    with open('volume/vars.json', 'r') as f:
        params = json.load(f)

    program = TextAreaField('Program', default=params['program'])
    p1 = StringField('p1', default=params['p1'], description='Pависимость в одномерном гнезде.')
    p2 = StringField('p2', default=params['p2'], description='Зависимость по i в двумерном гнезде.')
    p3 = StringField('p3', default=params['p3'], description='Зависимость по j в двумерном гнезде.')
    p4 = StringField('p4', default=params['p4'], description='Дуги из одномерного гнезда идут или нет в двумерное, дуги из двумерного идут или нет в трёхмерное.')
    p5 = StringField('p5', default=params['p5'], description='Зависимость в трёхмерном гнезде либо от первой итерации по k, либо от (k-1)-ой.')
    p6 = StringField('p6', default=params['p6'], description='Зависимость в трёхмерном гнезде либо вдоль i, либо вдоль j.')
    preview = SubmitField('Предпросмотр варианта')
    create = SubmitField('Генерация вариантов')


    # --------------debug settings--------------
    console = StringField('console')
    console_button = SubmitField('insert command')
    log_download = SubmitField('Скачать логи')

class ButtonForm(FlaskForm):
    submit = SubmitField('Создать пользователей')
