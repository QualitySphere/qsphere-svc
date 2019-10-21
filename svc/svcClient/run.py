#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_cors import CORS
import connexion
from db.db import db

import logging
from pony.orm import set_sql_debug
from apscheduler.schedulers.background import BackgroundScheduler as APScheduler
import requests


logging.basicConfig(level=logging.INFO, format='[ %(asctime)s ] %(levelname)s %(message)s')


def svc_job():
    # 调用同步接口
    requests.get(url='http://127.0.0.1:6001/api/issue/sync', timeout=30)


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
    scheduler.start()

    app.run(port=6001, debug=True)
