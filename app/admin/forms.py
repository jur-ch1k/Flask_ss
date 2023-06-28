from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import date
import json
import os


# class RegisterForm(FlaskForm):
#     username = StringField('Username')
#     password = PasswordField('Password')
#     password_repeat = PasswordField('Repeat password')
#     submit = SubmitField('register')


class RegisterUsers(FlaskForm):
    userNumber = StringField('Количество пользователей для добавления', default=0)
    year = date.today().strftime('%Y')
    defaultMask = 'ucmc' + year + 'ss'
    mask = StringField('Маска', default=defaultMask, validators=[DataRequired()])
    dirlist = os.listdir('volume/vars')
    dirlist.remove('not_a_task.txt')
    choices = [(val, val+': '+str(len(os.listdir('volume/vars/' + val)))+' шт.') for val in (sorted(dirlist))]
    vars_names = SelectField('Выбор вариант', choices=choices, validate_choice=False)
    give_var = BooleanField('Раздать варианты', default=True)
    submit = SubmitField('Создать пользователей')

    # --------------debug settings--------------
    # console = StringField('console')
    # console_button = SubmitField('insert command')
    # log_download = SubmitField('Скачать логи')

class VarsCreation(FlaskForm):
    with open('volume/vars.json', 'r') as f:
        params = json.load(f)

    program = TextAreaField('Program', default=params['program'])
    p1 = StringField('p1', default=params['p1'], description='Pависимость в одномерном гнезде.', validators=[DataRequired()])
    p2 = StringField('p2', default=params['p2'], description='Зависимость по i в двумерном гнезде.', validators=[DataRequired()])
    p3 = StringField('p3', default=params['p3'], description='Зависимость по j в двумерном гнезде.', validators=[DataRequired()])
    p4 = StringField('p4', default=params['p4'], description='Дуги из одномерного гнезда идут или нет в двумерное, дуги из двумерного идут или нет в трёхмерное.', validators=[DataRequired()])
    p5 = StringField('p5', default=params['p5'], description='Зависимость в трёхмерном гнезде либо от первой итерации по k, либо от (k-1)-ой.', validators=[DataRequired()])
    p6 = StringField('p6', default=params['p6'], description='Зависимость в трёхмерном гнезде либо вдоль i, либо вдоль j.', validators=[DataRequired()])
    var_name = StringField('Название варианта', default='new_variant', validators=[DataRequired()])
    give_var = BooleanField('Раздать новые варианты')
    preview = SubmitField('Предпросмотр варианта')
    create = SubmitField('Генерация вариантов')

    # --------------debug settings--------------
    # console = StringField('console')
    # console_button = SubmitField('insert command')
    # log_download = SubmitField('Скачать логи')

class VarsView(FlaskForm):
    dirlist = os.listdir('volume/vars')
    dirlist.remove('not_a_task.txt')
    choices = [(val, val) for val in (sorted(dirlist))]

    vars_names = SelectField('Выбор вариант', choices=choices, validate_choice=False)

    program = TextAreaField('Program', render_kw={'readonly': True})
    p1 = StringField('p1', render_kw={'readonly': True})
    p2 = StringField('p2', render_kw={'readonly': True})
    p3 = StringField('p3', render_kw={'readonly': True})
    p4 = StringField('p4', render_kw={'readonly': True})
    p5 = StringField('p5', render_kw={'readonly': True})
    p6 = StringField('p6', render_kw={'readonly': True})

    delete = SubmitField('Удалить вариант', render_kw={'disabled': True})
