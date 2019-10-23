#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pony.orm import db_session, select, get
from models.models import Connection, Project


@db_session
def list_project():
    """
    List All Projects
    :return:
    """
    items = select(p for p in Project if p.active != 'delete').order_by(Project.name)
    projects = list()
    for item in items:
        projects.append({
            'project_id': item.uuid,
            'project_name': item.name,
            'connection_id': item.connection.uuid,
            'active': item.active
        })
    return projects


@db_session
def get_project(project_id: str):
    """
    Get Project
    :param project_id:
    :return:
    """
    item = get(p for p in Project if str(p.uuid) == project_id)
    project = dict()
    if item:
        project = {
            "project_id": item.uuid,
            "project_name": item.name,
            'connection_id': item.connection.uuid,
            'active': item.active
        }
    return project


@db_session
def create_project(item: dict):
    """
    Create Project
    :param item:
    :return:
    """
    _connection = get(c for c in Connection if str(c.uuid) == item.get('connection_id'))
    _project = Project(
        connection=_connection,
        name=item.get('project_name'),
        active=item.get('active') if item.get('active') else 'enable'
    )
    return _project.uuid


@db_session
def update_project(project_id: str, item: dict):
    """
    Update Project
    :param project_id:
    :param item:
    :return:
    """
    _project = get(p for p in Project if str(p.uuid) == project_id)
    _project.name = item.get('project_name')
    _project.active = item.get('active') if item.get('active') else 'enable'
    _project.connection = get(c for c in Connection if str(c.uuid) == item.get('connection_id'))
    return _project.uuid


@db_session
def delete_project(project_id: dict):
    """
    Delete Project
    :param project_id:
    :return:
    """
    _project = get(p for p in Project if str(p.uuid) == project_id)
    _project.active = 'delete'
    return True


if __name__ == '__main__':
    print(u'This is a service of project')
