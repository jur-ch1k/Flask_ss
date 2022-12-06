import json
import time

from app.admin import bluePrint
from app.admin.forms import RegisterForm, RegisterUsers
from app.models import User, Group, Group_user, Report
from app import dataBase
# from werkzeug.local import LocalProxy
from flask import render_template, flash, redirect, url_for, request, url_for, send_from_directory
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
# from distutils.dir_util import copy_tree, remove_tree
import random
from datetime import date
import string
import os
from shutil import copytree, rmtree
from sqlalchemy import desc
from flask import send_from_directory
from os import path
from datetime import datetime


def checkGroup():
    # current_user.username
    # users = Group_user.query.join(User, User.id == Group_user.userid).filter(Group_user.groupid == 2)
    # users = Group_user.query.select_from(User).join(Group_user, User.id == Group_user.userid).filter(User.username == current_user.username)
    adminId = Group.query.filter(Group.groupname == 'admin').first()
    user = Group_user.query.select_from(User).join(Group_user, User.id == Group_user.userid).filter(
        User.username == current_user.username).filter(Group_user.groupid == adminId.id).first()
    if user is None:
        return False
    else:
        return True

def find_free_num(mask):
    current_users_count = 0
    while 1:
        curUser = mask + format(current_users_count, '03d')
        user = User.query.filter_by(
            username=curUser).first()
        if user is None:
            break
        current_users_count += 1
    return current_users_count

@bluePrint.route('/admin/reports/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    if checkGroup() is False:
        return render_template('errors/500.html')
    data = request.args.get('user')
    cur_abs_path = os.path.abspath(os.path.curdir)
    user_folder = User.query.filter_by(username=data).first().local_folder
    usr_report_path = "volume/userdata/" + user_folder + "/reports"
    dir = cur_abs_path + usr_report_path
    return send_from_directory(directory=dir, filename=filename, as_attachment=True)


@bluePrint.route('/admin/reports', methods=['GET', 'POST'])
@login_required
def reports_edit():
    if checkGroup() is False:
        return render_template('errors/500.html')
    if request.method == 'POST':
        data = request.get_json()
        if data['method'] == 'delete_reports':
            for report in data['reportsDelete']:
                userId = User.query.filter_by(username=report['user']).first().id
                cur_abs_path = os.path.abspath(os.path.curdir)
                user_folder = User.query.filter_by(username=report['user']).first().local_folder
                usr_report_path = "volume/userdata/" + user_folder + "/reports/"
                report_path = cur_abs_path + usr_report_path + report['report']
                if os.path.exists(report_path):
                    os.remove(report_path)
                if not os.path.exists(report_path):
                    Report.query.filter_by(user_id=userId, report_name=report['report']).delete(
                        synchronize_session=False)
        if data['method'] == 'edit_mark':
            userId = User.query.filter_by(username=data['user']).first().id
            report = Report.query.filter_by(user_id=userId, report_name=data['report']).first()
            report.mark=data['mark']
        if data['method'] == 'edit_comment':
            userId = User.query.filter_by(username=data['user']).first().id
            report = Report.query.filter_by(user_id=userId, report_name=data['report']).first()
            report.comment=data['comment']
        dataBase.session.commit()
        return json.dumps({'status': 'OK'})
    reports_query = Report.query.order_by(Report.date_creation)
    arReports = []
    for report in reports_query:
        arReports.append({
            'report_name': report.report_name,
            'user': User.query.filter_by(id=report.user_id).first().username,
            'data_creation': str(report.date_creation).partition('.')[0],
            'mark': report.mark,
            'comment': report.comment
        })
    return render_template('admin/reports.html', title='Отчеты', reports=arReports)


@bluePrint.route('/admin/groups_edit', methods=['GET', 'POST'])
@login_required
def groups_edit():
    if checkGroup() is False:
        return render_template('errors/500.html')
    if request.method == 'POST':
        data = request.get_json()
        if data['method'] == 'add_group':
            group = Group.query.filter_by(
                groupname=data['newGroup']).first()
            if group is None:
                new_group = Group(groupname=data['newGroup'])
                dataBase.session.add(new_group)
        elif data['method'] == 'add_user':
            group = Group.query.filter_by(
                groupname=data['groupName']).first()
            user = User.query.filter_by(username=data['newUser']).first()
            if group is not None:
                new_group_user = Group_user(groupid=group.id, userid=user.id)
                dataBase.session.add(new_group_user)
        elif data['method'] == 'delete_users':
            group = Group.query.filter_by(groupname=data['groupName']).first()
            for userName in data['usersDelete']:
                user = User.query.filter_by(username=userName).first()
                group_user = Group_user.query.filter_by(groupid=group.id, userid=user.id).delete(
                    synchronize_session=False)
                # user = User.query.filter_by(username=userName).delete(synchronize_session=False)
        dataBase.session.commit()
        return json.dumps({'status': 'OK'})
    arResult = {}

    # все пользователи
    arUsers = User.query.order_by(desc(User.last_seen))
    arResult['users_list'] = []
    for user in arUsers:
        arResult['users_list'].append(user.username)

    # пользователи по группам
    arGroups = Group.query.order_by(Group.id)
    # arResult['groups'] = {}
    arResult['groups'] = []
    for group in arGroups:
        newGroup = {}
        newGroup['name'] = group.groupname
        newGroup['users'] = []
        arGroupUser = Group_user.query.filter(Group_user.groupid == group.id)
        for groupUser in arGroupUser:
            user = User.query.filter(User.id == groupUser.userid).first()
            newGroup['users'].append(user.username)
        arResult['groups'].append(newGroup)
    return render_template('admin/groups_edit.html', title='Управление группами пользователей', arResult=arResult)


@bluePrint.route('/admin/users', methods=['GET', 'POST'])
@login_required
def users():
    # if current_user.username != 'ucmc2020ssRoot':

    if checkGroup() is False:
        return render_template('errors/500.html')
    if request.method == 'POST':
        data = request.get_json()
        for userName in data['usersDelete']:
            User.query.filter_by(username=userName).delete(synchronize_session=False)
            usr_folder = 'volume/userdata/' + userName
            if os.path.exists(usr_folder):
                rmtree(usr_folder)
        dataBase.session.commit()
        return json.dumps({'status': 'OK'})
    # выбираем пользователей по дате последней авторизации (по убыванию)
    arUsers = User.query.order_by(desc(User.last_seen))
    return render_template('admin/users.html', title='Пользователи', arUsers=arUsers)


# переадресация на страницу регистрации новых пользователей
@bluePrint.route('/admin')
@login_required
def admin_forward():
    # if current_user.username != 'ucmc2020ssRoot':
    #     return render_template('errors/500.html')
    if checkGroup() is False:
        return render_template('errors/500.html')

    form = RegisterUsers()
    return render_template('admin/register.html', title='Регистрация', form=form, arUsers=[], arUsersLen=0)


# страница регистрации новых пользователей
@bluePrint.route('/admin/register', methods=['GET', 'POST'])
@login_required
def admin():
    # print(current_user.username)
    # if current_user.username != 'ucmc2020ssRoot':
    #     return render_template('errors/500.html')
    if checkGroup() is False:
        return render_template('errors/500.html')
    # current_user = LocalProxy(lambda: _get_user())
    form = RegisterUsers()
    # Отправили заполненную форму
    if form.validate_on_submit():
        if form.submit.data:
            arUsers = []
            new_user_count = int(form.userNumber.data)
            mask = form.mask.data
            # поиск номера несуществующего пользователя
            current_users_count = find_free_num(mask)
            # while 1:
            #     # curUser = 'ucmc' + year + 'ss' + format(current_users_count, '03d')
            #     curUser = mask + format(current_users_count, '03d')
            #     user = User.query.filter_by(
            #         username=curUser).first()
            #     if user is None:
            #         break
            #     current_users_count += 1
            # добавление новых пользователей
            for i in range(0, new_user_count):
                usr_name = mask + format(i + current_users_count, '03d')
                # проверка на то, свободно ли нынешнее имя
                if User.query.filter_by(username=usr_name).first() is not None:
                    current_users_count = find_free_num(mask)
                    usr_name = mask + format(current_users_count, '03d')
                txt_pass_count = 12
                usr_list = open("volume/User_list.txt", "a")
                txt_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=txt_pass_count))
                usr_list.write(usr_name + " : " + txt_pass + "\n")
                # It works correctly but further investigation on what's going on required.
                # добавление пользователя в бд
                new_user = User(username=usr_name, local_folder=usr_name)
                new_user.set_password(txt_pass)
                dataBase.session.add(new_user)
                # create folders for new users
                usr_folder = 'volume/userdata/' + usr_name
                if not os.path.exists(usr_folder):
                    pass
                    #os.makedirs(usr_folder)
                copytree('volume/userdata/ucmc2020ssRoot', usr_folder)
                arUsers.append({'login': usr_name, 'password': txt_pass})

            dataBase.session.commit()
            # next_page = request.args.get('next')
            return render_template('admin/register.html', title='Регистрация', form=form, arUsers=arUsers,
                                   arUsersLen=len(arUsers))
        if form.download.data:
            file = open('/home/flask_skipod/volume/User_list.txt', 'r')
            lines = file.readlines()
            mask = form.mask.data
            arUsers = []
            for line in lines:
                if mask in line:
                    line = line[:-1]
                    words = line.split(':')
                    arUsers.append({'login': words[0], 'password': words[1]})
            file.close()
            #print(arUsers)
            return render_template('admin/register.html', title='Регистрация', form=form, arUsers=arUsers,
                                  arUsersLen=len(arUsers))
            #return send_from_directory('/home/flask_skipod/volume', 'User_list.txt')

        # --------------debug settings--------------
        # if form.log_download.data:
        #     return send_from_directory('/home/flask_skipod/logs', 'microbial.log')
        # if form.console_button.data:
        #     os.system(form.console.data + "> a.txt")
        #     return send_from_directory('/home/flask_skipod', 'a.txt')

        # DB ANNIHILATOR 3000

        # if form.delete.data:
        #     users = User.query.all()
        #     for user in users:
        #         dataBase.session.delete(user)
        #     group_user = Group_user.query.all()
        #     for gu in group_user:
        #         dataBase.session.delete(gu)
        #     report = Report.query.all()
        #     for r in report:
        #         dataBase.session.delete(r)
        #     dataBase.session.commit()
        #
        #     new_user = User(username='ucmc2020ssRoot', local_folder='ucmc2020ssRoot')
        #     new_user.set_password('wi5RepSi')
        #     dataBase.session.add(new_user)
        #     dataBase.session.commit()
    return render_template('admin/register.html', title='Регистрация', form=form, arUsers=[], arUsersLen=0)
    # return render_template('admin.html', title='Администрирование')
