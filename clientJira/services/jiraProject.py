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
            _project.uuid == project_id
        )
    return {
        'status': 200,
        'title': 'Succeed To Get Project',
        'detail': item
    }, 200


def create_project(project: dict):
    with db_session:
        _project = Project(
            connection=project.get('connectionId'),
            name=project.get('projectName'),
            version=project.get('productVersion'),
            status=project.get('status') if project.get('status') else 'active'
            # sprints=project.get('features'),
            # rcs=project.get('rcs'),
            # issue_types=project.get('issueTypes'),
            # issue_categories=project.get('issueCategories')
        )
    return {
        'status': 200,
        'title': 'Succeed To Create Project',
        'detail': {
            'projectId': _project.uuid
        }
    }, 200


if __name__ == '__main__':
    print(u'This is a service of JIRA project')
