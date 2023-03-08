from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import date


class RegisterForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    password_repeat = PasswordField('Repeat password')
    submit = SubmitField('register')


class RegisterUsers(FlaskForm):
    userNumber = StringField('Количество пользователей для добавления', default=0)
    # password = PasswordField('Password')
    # password_repeat = PasswordField('Repeat password')
    year = date.today().strftime('%Y')
    defaultMask = 'ucmc' + year + 'ss'
    mask = StringField('Маска', default=defaultMask)
    submit = SubmitField('Создать пользователей')
    # download = SubmitField('Скачать')

class VarsCreation(FlaskForm):
    # use_last = BooleanField('Использовать предыдущее задание')
    program = TextAreaField('Program', default="""for(i = 2; i <= n+1; ++i)
   C[i] = C[i+p1] + D[i];
for(i = 2; i <= n+1; ++i)
   for(j = 2; j <= m+1; ++j)
      B[i][j] = B[i+p2][j+p3] + p4*C[n+1];
for(i = 2; i <= n+1; ++i) {
   A[i][1][1]=C[i]+(1-p4)*B[i][m+1];
   for(j = 2; j <= m+1; ++j) {
      for(k = 1; k <= n; ++k)
         A[i][j][k] = A[i][j][k] + p5*A[i-p6][j-(1-p6)][k] + (1-p5)*A[i-(1-p6)][j-p6][k-1];
}""")
    p1 = StringField('p1', default='-1 1', description='Pависимость в одномерном гнезде.')
    p2 = StringField('p2', default='-2 -1 0 1', description='Зависимость по i в двумерном гнезде.')
    p3 = StringField('p3', default='-2 -1 0 1', description='Зависимость по j в двумерном гнезде.')
    p4 = StringField('p4', default='0 1', description='Дуги из одномерного гнезда идут или нет в двумерное, дуги из двумерного идут или нет в трёхмерное.')
    p5 = StringField('p5', default='0 1', description='Зависимость в трёхмерном гнезде либо от первой итерации по k, либо от (k-1)-ой.')
    p6 = StringField('p6', default='0 1', description='Зависимость в трёхмерном гнезде либо вдоль i, либо вдоль j.')
    create = SubmitField('Генерация вариантов')


    # --------------debug settings--------------
    # console = StringField('console')
    # console_button = SubmitField('insert command')
    # log_download = SubmitField('Скачать логи')

class ButtonForm(FlaskForm):
    submit = SubmitField('Создать пользователей')
