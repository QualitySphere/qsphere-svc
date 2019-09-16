#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import connexion
from flask import current_app
from pony.orm import db_session, select, get
from models.models import Connection, Project
from clientJira.utils.jiraClient import JiraSession


@db_session
def list_projects():
    items = select(p for p in Project if p.active == 'enable').order_by(Project.name)
    if items:
        projects = list()
        for item in items:
            projects.append({
                'project_id': item.uuid,
                'project_name': item.name
            })
        return {
            'title': 'Succeed To List Projects',
            'detail': {
                'count': items.count(),
                'results': projects,
            }
        }, 200
    else:
        return {
            'title': 'Project Not Found',
        }, 404


@db_session
def get_project(project_id: str):
    item = get(p for p in Project if str(p.uuid) == project_id)
    if item:
        return {
            'title': 'Succeed To Get Project',
            'detail': {
                "project_name": item.name,
            }
        }, 200
    else:
        return {
            'title': 'Project Not Found',
        }, 404


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
