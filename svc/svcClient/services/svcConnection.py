#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pony.orm import db_session, get, select
from models.models import Connection
from utils.jiraClient import JiraSession


@db_session
def create_connection(server_info: dict):
    """
    Create Connection With Bug/Case Manage Server
    :param server_info:
    :return:
    """
    _connection_name = server_info.get('connection_name')
    _issue_server = {
        'type': server_info.get('issue_server').get('type'),
        'host': server_info.get('issue_server').get('host'),
        'account': server_info.get('issue_server').get('account'),
        'password': server_info.get('issue_server').get('password'),
    }
    _case_server = {
        'type': server_info.get('case_server').get('type'),
        'host': server_info.get('case_server').get('host'),
        'account': server_info.get('case_server').get('account'),
        'password': server_info.get('case_server').get('password'),
    }
    if _issue_server.get('type') == 'jira':
        with JiraSession(_issue_server.get('host'), _issue_server.get('account'), _issue_server.get('password')) as jira_session:
            _current_user = jira_session.get_user()
    else:
        raise Exception('Only Support JIRA Issue')
    _connection = Connection(
        name=_connection_name,
        issue_server=_issue_server,
        case_server=_case_server
    )
    return _connection.uuid


@db_session
def update_connection(connection_id: str, server_info: dict):
    """
    Update Connection With Bug/Case Manage Server
    :param connection_id:
    :param server_info:
    :return:
    """
    _connection_name = server_info.get('connection_name')
    _issue_server = {
        'type': server_info.get('issue_server').get('type'),
        'host': server_info.get('issue_server').get('host'),
        'account': server_info.get('issue_server').get('account'),
        'password': server_info.get('issue_server').get('password'),
    }
    _case_server = {
        'type': server_info.get('case_server').get('type'),
        'host': server_info.get('case_server').get('host'),
        'account': server_info.get('case_server').get('account'),
        'password': server_info.get('case_server').get('password'),
    }
    _connection = get(c for c in Connection if str(c.uuid) == connection_id)
    if _issue_server.get('type') == 'jira':
        with JiraSession(_issue_server.get('host'), _issue_server.get('account'), _issue_server.get('password')) as jira_session:
            _current_user = jira_session.get_user()
    else:
        raise Exception('Only Support JIRA Issue')
    _connection.name = _connection_name
    _connection.issue_server = _issue_server
    _connection.case_server = _case_server
    return _connection.uuid


@db_session
def list_connection():
    """
    List All Active Connection Info
    :return:
    """
    items = select(c for c in Connection if c.active == 'enable')
    connections = list()
    for item in items:
        connections.append({
            'connection_id': item.uuid,
            'connection_name': item.name,
            'issue_server': {
                'type': item.issue_server.get('type'),
                'host': item.issue_server.get('host'),
                'account': item.issue_server.get('account'),
            },
            'case_server': {
                'type': item.case_server.get('type'),
                'host': item.case_server.get('host'),
                'account': item.case_server.get('account'),
            }
        })
    return connections


@db_session
def get_connection(connection_id: str):
    """
    Get Connection
    :param connection_id:
    :return:
    """
    item = get(c for c in Connection if str(c.uuid) == connection_id)
    if item:
        _connection = {
            'connection_id': item.uuid,
            'connection_name': item.name,
            'issue_server': {
                'type': item.issue_server.get('type'),
                'host': item.issue_server.get('host'),
                'account': item.issue_server.get('account'),
            },
            'case_server': {
                'type': item.case_server.get('type'),
                'host': item.case_server.get('host'),
                'account': item.case_server.get('account'),
            },
            'active': item.active,
        }
    else:
        _connection = {}
    return _connection


@db_session
def delete_connection(connection_id: str):
    """
    Delete Connection
    :param connection_id:
    :return:
    """
    item = get(c for c in Connection if str(c.uuid) == connection_id)
    if item:
        item.active = 'delete'
    return True


if __name__ == '__main__':
    print(u'This is a service of connection')
