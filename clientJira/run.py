#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_cors import CORS
import connexion
from clientJira.db.db import db
import logging
from pony.orm import set_sql_debug
# from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler as APScheduler
import requests


logging.basicConfig(level=logging.INFO, format='[ %(asctime)s ] %(levelname)s %(message)s')


def jira_job():
    requests.get(url='http://127.0.0.1:6001/api/jira/sprint/sync', timeout=30)


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
    app.add_api("jira-client.yaml")
    set_sql_debug(True)
    db.generate_mapping(create_tables=True)
    scheduler = APScheduler()
    scheduler.add_job(func=jira_job, id='jira_job', trigger='interval', hours=1, replace_existing=True)
    scheduler.start()
    app.run(port=6001, debug=True)
