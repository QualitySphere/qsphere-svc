#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_cors import CORS
import connexion
from clientJira.db.db import db

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
    db.generate_mapping(create_tables=True)
    app.run(port=6001)
