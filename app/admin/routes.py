from app.admin import bluePrint
from app.admin.forms import RegisterUsers, VarsCreation
from app.models import User, Group, Group_user, Report
from app import dataBase
from flask import render_template, flash, redirect, url_for, request, url_for, send_from_directory
from flask_login import current_user, login_required
from shutil import copytree, rmtree
from sqlalchemy import desc
from flask import send_from_directory
import random
import string
import sympy
import tqdm
import json
import os
import re


def isAdmin():
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

def isTeacher():
    teacherId = Group.query.filter(Group.groupname == 'teacher').first()
    user = Group_user.query.select_from(User).join(Group_user, User.id == Group_user.userid).filter(
        User.username == current_user.username).filter(Group_user.groupid == teacherId.id).first()
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


def pprint(s=""):
    # print(s) # uncomment it to see debug messagess
    return


def generate(program, bounds):
    """generate all possible combinations of params"""
    result = [program]

    for name, values in bounds:
        new_result = []
        for old_program in result:
            for value in values:
                new_result.append(old_program.replace(name, str(value)))

        result = new_result
    return result


re_right_part = re.compile(r'.*=(.*);\n')
re_index = re.compile(r'(\[[^]]+\])')


def _simplify_right_part(right_part):
    replace_dict = {}

    letters = [chr(ord('Z') - x) for x in range(20)]
    letter_index = 0

    for index in re_index.findall(right_part):
        replace_dict[index] = letters[letter_index]
        letter_index += 1

    result = right_part

    pprint()
    pprint(right_part)

    for k, v in replace_dict.items():
        result = result.replace(k, v)
    pprint(result)

    result = str(sympy.simplify(result))
    pprint(result)

    for k, v in replace_dict.items():
        index = k.strip('[]')
        simple_index = str(sympy.simplify(index))

        result = result.replace(v, f"[{simple_index}]")
    pprint(result)
    pprint()

    return result


def simplify(program):
    """simplify all things like (1-1)*A, A[i+-1] and so on"""
    result = program

    for right_part in re_right_part.findall(program):
        result = result.replace(right_part, " " + _simplify_right_part(right_part))

    return result


def generate_vars(program, bounds, output_dir='volume/vars', preview=False):
    all_vars = generate(program, bounds)

    if preview is False:
        try:
            os.mkdir(output_dir)
        except FileExistsError:
            rmtree(output_dir)
            os.mkdir(output_dir)

    for i, program in tqdm.tqdm(enumerate(all_vars)):
        if preview:
            return simplify(program)
        with open(f"{output_dir}/program_{str(i)}.c", "w") as fd:
            fd.write(simplify(program))


@bluePrint.route('/admin/reports/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    if (isAdmin() or isTeacher()) is False:
        return render_template('errors/500.html')
    data = request.args.get('user')
    cur_abs_path = os.path.abspath(os.path.curdir)
    user_folder = User.query.filter_by(username=data).first().local_folder
    usr_report_path = "/volume/userdata/" + user_folder + "/reports"
    dir = cur_abs_path + usr_report_path
    return send_from_directory(directory=dir, filename=filename, as_attachment=True)


@bluePrint.route('/admin/reports', methods=['GET', 'POST'])
@login_required
def reports_edit():
    if isAdmin() is False:
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
            report.mark = data['mark']
        if data['method'] == 'edit_comment':
            userId = User.query.filter_by(username=data['user']).first().id
            report = Report.query.filter_by(user_id=userId, report_name=data['report']).first()
            report.comment = data['comment']
        if data['method'] == 'edit_name':
            userId = User.query.filter_by(username=data['user']).first().id
            report = Report.query.filter_by(user_id=userId, report_name=data['report']).first()
            report.teacher_name = data['teacher_name']
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
            'comment': report.comment,
            'var_num': report.var_num,
            'teacher_name': report.teacher_name
        })
    return render_template('admin/reports.html', title='Отчеты', reports=arReports)


@bluePrint.route('/admin/groups_edit', methods=['GET', 'POST'])
@login_required
def groups_edit():
    if isAdmin() is False:
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
        newGroup = {'name': group.groupname, 'users': []}
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

    if isAdmin() is False:
        return render_template('errors/500.html')
    if request.method == 'POST':
        data = request.get_json()

        if ('usersDelete' in data.keys()):
            for userName in data['usersDelete']:
                usr = User.query.filter_by(username=userName).first()
                User.query.filter_by(username=userName).delete(synchronize_session=False)
                Report.query.filter_by(user_id=usr.id).delete(synchronize_session=False)
                Group_user.query.filter_by(userid=usr.id).delete(synchronize_session=False)
                usr_folder = 'volume/userdata/' + userName
                if os.path.exists(usr_folder):
                    rmtree(usr_folder)

        if ('usersNewPassWord' in data.keys()):
            usr_list = open("volume/User_list.txt", "w")
            arusr = {}
            for userName in data['usersNewPassWord']:
                usr = User.query.filter_by(username=userName).first()
                txt_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                usr.set_password(txt_pass)
                usr_list.write(userName + ' : ' + txt_pass + '\n')
                arusr[userName] = txt_pass
            usr_list.close()

        dataBase.session.commit()
        return json.dumps({'status': 'OK'})
    # выбираем пользователей по дате последней авторизации (по убыванию)
    arUsers = User.query.order_by(desc(User.last_seen))
    return render_template('admin/users.html', title='Пользователи', arUsers=arUsers)


@bluePrint.route('/admin/users/download')
@login_required
def download_var():
    if isAdmin() is False:
        return render_template('errors/500.html')
    return send_from_directory(directory='/home/flask_skipod/volume', filename='User_list.txt', as_attachment=True)


# переадресация на страницу регистрации новых пользователей
@bluePrint.route('/admin')
@login_required
def admin_forward():
    # if current_user.username != 'ucmc2020ssRoot':
    #     return render_template('errors/500.html')
    if isAdmin() is False:
        return render_template('errors/500.html')

    return render_template('admin/welcome.html', title='Панель администратора')


# страница регистрации новых пользователей
@bluePrint.route('/admin/register', methods=['GET', 'POST'])
@login_required
def admin():
    if isAdmin() is False:
        return render_template('errors/500.html')
    form = RegisterUsers()
    dirlist = os.listdir('volume/vars')
    dirlist.remove('not_a_task.txt')
    form.var_folder.choices = [(val, val) for val in (sorted(dirlist))]

    # Отправили заполненную форму
    if form.validate_on_submit():
        if form.submit.data:
            arUsers = []
            new_user_count = int(form.userNumber.data)
            mask = form.mask.data
            # поиск номера несуществующего пользователя
            current_users_count = find_free_num(mask)
            old_i = 0
            try:
                var_num = len(os.listdir('volume/vars/' + form.var_folder.data))
            except FileNotFoundError:
                var_num = 0

            for i in range(0, new_user_count):
                usr_name = mask + format(i + current_users_count - old_i, '03d')
                # проверка на то, свободно ли нынешнее имя
                if User.query.filter_by(username=usr_name).first() is not None:
                    current_users_count = find_free_num(mask)
                    usr_name = mask + format(current_users_count, '03d')
                    old_i = i
                txt_pass_count = 12
                txt_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=txt_pass_count))
                # It works correctly but further investigation on what's going on required.
                # добавление пользователя в бд
                if form.give_var.data:
                    new_user = User(username=usr_name, local_folder=usr_name,
                                    var_num=i % var_num,
                                    var_file=form.var_folder.data + '/program_' + str(i % var_num) + '.c')
                else:
                    new_user = User(username=usr_name, local_folder=usr_name,
                                    var_num= -1, var_file='not_a_task.txt')
                new_user.set_password(txt_pass)
                dataBase.session.add(new_user)
                # create folders for new users
                usr_folder = 'volume/userdata/' + usr_name
                if not os.path.exists(usr_folder):
                    copytree('new_user_folder', usr_folder)
                arUsers.append({'login': usr_name, 'password': txt_pass})

            dataBase.session.commit()
            return render_template('admin/register.html', title='Регистрация', form=form,
                                   arUsers=arUsers, arUsersLen=len(arUsers))

        # --------------debug settings--------------
        # if form.log_download.data:
        #     return send_from_directory('/home/flask_skipod/logs', 'microbial.log')
        # if form.console_button.data:
        #     os.system(form.console.data + "> a.txt")
        #     return send_from_directory('/home/flask_skipod', 'a.txt')

        # -----------DB ANNIHILATOR 3000------------
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
    return render_template('admin/register.html', title='Регистрация', form=form,
                           arUsers=[], arUsersLen=0)


@bluePrint.route('/admin/variants_generation', methods=['GET', 'POST'])
@login_required
def generate_vars_page():
    if isAdmin() is False:
        return render_template('errors/500.html')
    var_form = VarsCreation()
    # dirlist = os.listdir('volume/vars')
    # dirlist.remove('not_a_task.txt')

    # Отправили заполненную форму
    if var_form.validate_on_submit():
        params = {}
        bounds = []

        if var_form.preview.data or var_form.create.data:
            new_params = {}
            old_params = {}
            with open('volume/vars.json') as f:
                old_params = json.load(f)
            new_params = {"program": var_form.program.data.replace('\r', ''),
                          "p1": var_form.p1.data,
                          "p2": var_form.p2.data,
                          "p3": var_form.p3.data,
                          "p4": var_form.p4.data,
                          "p5": var_form.p5.data,
                          "p6": var_form.p6.data
                          }
            if old_params != new_params:
                with open('volume/vars.json', 'w') as f:
                    json.dump(new_params, f)
            params = new_params
            bounds = [
                ("p1", [int(s) for s in params['p1'].rstrip().lstrip().split()]),
                ("p2", [int(s) for s in params['p2'].rstrip().lstrip().split()]),
                ("p3", [int(s) for s in params['p3'].rstrip().lstrip().split()]),
                ("p4", [int(s) for s in params['p4'].rstrip().lstrip().split()]),
                ("p5", [int(s) for s in params['p5'].rstrip().lstrip().split()]),
                ("p6", [int(s) for s in params['p6'].rstrip().lstrip().split()]),
            ]

        if var_form.preview.data:
            return render_template('admin/variants_generation.html', title='Создание вариантов', form=var_form,
                                   preview=generate_vars(params['program'], bounds, preview=True))
        if var_form.create.data:
            generate_vars(params['program'], bounds, output_dir='volume/vars/' + var_form.var_folder.data)
            users = User.query.all()
            if var_form.give_var.data:
                try:
                    var_num = len(os.listdir('volume/vars/' + var_form.var_folder.data))
                except FileNotFoundError:
                    var_num = 0
                for i, user in enumerate(users):
                    if user.var_num != -1:
                        user.var_num = i % var_num
                        user.var_file = var_form.var_folder.data + '/program_' + str(i % var_num) + '.c'
                dataBase.session.commit()
            return render_template('admin/generation_success.html', title='Создание вариантов', form=var_form,
                                   arUsers=[], arUsersLen=0, preview=False)

        # --------------debug settings--------------
        # if var_form.log_download.data:
        #     return send_from_directory('/home/flask_skipod/logs', 'microbial.log')
        # if var_form.console_button.data:
        #     os.system(var_form.console.data + "> a.txt")
        #     return send_from_directory('/home/flask_skipod', 'a.txt')

    return render_template('admin/variants_generation.html', title='Создание вариантов', form=var_form,
                           arUsers=[], arUsersLen=0, preview=False)
