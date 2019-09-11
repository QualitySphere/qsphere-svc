#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import connexion
from flask import current_app
from pony.orm import db_session, select, get
from models.models import Connection, Project
from clientJira.utils.jiraClient import JiraSession


def list_project():
    with db_session:
        items = select(
            _project for _project in Project if
            _project.status == 'active'
        ).order_by(Project.name)
    return {
        'status': 200,
        'title': 'Succeed To Get Project',
        'detail': items
    }, 200


def get_project(project_id: str):
    with db_session:
        item = get(
            _project for _project in Project if
            str(_project.uuid) == project_id
        )
    return {
        'status': 200,
        'title': 'Succeed To Get Project',
        'detail': {
            "project_name": item.name,
        }
    }, 200


def create_project(item: dict):
    with db_session:
        _connection = get(c for c in Connection if str(c.uuid) == item.get('connection_id'))
        _project = Project(
            connection=_connection,
            name=item.get('project_name'),
            active=item.get('active') if item.get('active') else 'enable'
        )
    return {
        'status': 200,
        'title': 'Succeed To Create Project',
        'detail': {
            'project_id': _project.uuid
        }
    }, 200


if __name__ == '__main__':
    print(u'This is a service of JIRA project')
