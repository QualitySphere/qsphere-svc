#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_cors import CORS
import connexion
from db.db import db
import os
import yaml
import json
import logging
from pony.orm import set_sql_debug
from apscheduler.schedulers.background import BackgroundScheduler as APScheduler
import requests
from utils.wechatRobot import WechatRobotSender


if os.getenv('DEBUG'):
    logging.basicConfig(level=logging.DEBUG, format='[ %(asctime)s ] %(levelname)s %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='[ %(asctime)s ] %(levelname)s %(message)s')


def svc_job():
    # 调用同步接口
    requests.get(url='http://127.0.0.1:6001/api/issue/sync', timeout=30)


def _generate_bug_status_markdown_text(bug_info: dict):
    bug_info.get('sprint_name')
    bug_markdown_text = '\n'.join([
        '#### %s 缺陷最新状态' % bug_info.get('sprint_name'),
        '- <font color=\"warning\">待修复: %s</font>' % bug_info.get('issue_status').get('fixing'),
        '- <font color=\"comment\">待验证: %s</font>' % bug_info.get('issue_status').get('fixed'),
        '- <font color=\"info\">已验证: %s</font>' % bug_info.get('issue_status').get('verified'),
        '\n'
    ])
    return bug_markdown_text


def wechat_robot_job():
    # 微信机器人消息
    if os.getenv('WECHAT_ROBOT_KEY'):
        try:
            bugs = requests.get(url='http://127.0.0.1:6001/api/issue/status', timeout=30).json()
            robot = WechatRobotSender(robot_key=os.getenv('WECHAT_ROBOT_KEY'))
            markdown_text = ''
            for bug in bugs.get('detail'):
                markdown_text = markdown_text + _generate_bug_status_markdown_text(bug)
            robot.send_markdown_msg(markdown_text=markdown_text)
        except Exception as e:
            logging.error(str(e))
            return False
    return True


def machine_check_job():
    vms = list()
    # Load machine list from YAML file
    machine_list_file = os.path.join('svcClient', 'specs', 'machine-list.yaml')
    machine_status_file = os.path.join('svcClient', 'specs', 'machine-status.json')
    with open(machine_list_file, 'r') as f:
        vms_list = yaml.full_load(f.read())
    # Check machine in machine list
    for vm_name, vm_ip in vms_list.items():
        vm = {
            'name': vm_name,
            'ip': vm_ip,
            'status': 'OFFLINE'
        }
        output = os.system('ping -c 1 -W 1 ' + vm_ip)
        if output == 0:
            vm['status'] = 'ONLINE'
        vms.append(vm)
    # Generate machine status JSON file
    with open(machine_status_file, 'w') as f:
        f.write(json.dumps(vms))
    return True


if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    options = {
        "swagger_ui": True
    }
    app = connexion.FlaskApp(
        __name__,
        specification_dir='specs/',
        options=options
    )
    app.add_api("swagger.yaml")

    # DB mapping
    set_sql_debug(True)
    db.generate_mapping(create_tables=True)

    # schedule task, execute hourly
    scheduler = APScheduler()
    scheduler.add_job(func=svc_job, id='svc_job', trigger='interval', hours=1, replace_existing=True)
    # scheduler.add_job(func=machine_check_job, id='machine_check_job', trigger='interval', seconds=600, replace_existing=True)
    # scheduler.add_job(func=wechat_robot_job, id='wechat_robot_job', trigger='cron', hour=1, minute=30, replace_existing=True)  # UTC Date
    scheduler.start()

    # Start flask app
    app.run(port=80, debug=True)
