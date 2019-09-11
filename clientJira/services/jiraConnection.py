#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import connexion
from flask import current_app
from pony.orm import db_session, select, get
from models.models import Connection
from clientJira.utils.jiraClient import JiraSession


def create_connection(server_info: dict):
    _server = server_info.get('server')
    _account = server_info.get('account')
    _password = server_info.get('password')
    with JiraSession(_server, _account, _password) as jira_session:
        _current_user = jira_session.get_user()
        with db_session:
            _connection = Connection(
                type='jira',
                server=_server,
                account=_account,
                password=_password
            )
    return {
        'status': 200,
        'title': 'Create Connection Succeed',
        'detail': {
            'connection_id': _connection.uuid,
            'jira_user': _connection.account,
        }
    }, 200


def get_connection():
    with db_session:
        _connection = get(item for item in Connection if item.type == 'jira')
    return {
        'status': 200,
        'title': 'Get Connection Succeed',
        'detail': {
            'connection_id': _connection.uuid,
            'server': _connection.server,
            'account': _connection.account,
        }
    }, 200


if __name__ == '__main__':
    print(u'This is a service of JIRA connection')
