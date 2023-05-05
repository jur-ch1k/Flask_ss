from app.teacher import bluePrint
from app.models import User, Group, Group_user, Report
from app import dataBase
from flask import render_template, request
from flask_login import current_user, login_required
from app.admin.routes import isAdmin, isTeacher
import json
import os


@bluePrint.route('/teacher', methods=['GET', 'POST'])
@login_required
def t_reports_edit():
    if (isAdmin() or isTeacher()) is False:
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
            'var_num': report.var_num
        })
    return render_template('teacher/reports.html', title='Отчеты', reports=arReports)

