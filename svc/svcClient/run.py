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


logging.basicConfig(level=logging.INFO, format='[ %(asctime)s ] %(levelname)s %(message)s')


def svc_job():
    # 调用同步接口
    requests.get(url='http://127.0.0.1:6001/api/issue/sync', timeout=30)


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
    app.add_api("svc-client.yaml")

    # 关联数据库
    set_sql_debug(True)
    db.generate_mapping(create_tables=True)

    # 创建定时任务, 每小时执行一次同步
    scheduler = APScheduler()
    scheduler.add_job(func=svc_job, id='svc_job', trigger='interval', hours=1, replace_existing=True)
    scheduler.add_job(func=machine_check_job, id='machine_check_job', trigger='interval', seconds=600, replace_existing=True)
    scheduler.start()

    app.run(port=6001, debug=True)
