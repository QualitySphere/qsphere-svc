#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Project Model
# uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
# name = Required(str)
# tracker = Optional(Json)  # {'issue': 'UUID', 'case': 'UUID'}
# project = Optional(Json)  # {'issue': {'key': 'value'}, 'case': {'key': 'value'}}
# status = Required(str, default='active')  # active, disable, delete
# sprints = Set('Sprint')


from pony.orm import db_session, select, get
from models.models import Tracker, Project


@db_session
def list_project():
    """
    List All Projects
    :return:
    """
    items = select(p for p in Project if p.status != 'delete').order_by(Project.name)
    projects = list()
    for item in items:
        projects.append({
            'id': item.uuid,
            'name': item.name,
            'tracker': {
                'issue': {
                    'id': item.tracker.get('issue'),
                    'name': get(t for t in Tracker if str(t.uuid) == item.tracker.get('issue')).name,
                },
                'case': {
                    'id': item.tracker.get('case'),
                    'name': get(t for t in Tracker if str(t.uuid) == item.tracker.get('case')).name,
                }
            },
            'project': {
                'issue': {
                    'key': item.project.get('issue').get('key'),
                    'value': item.project.get('issue').get('value'),
                },
                'case': {
                    'key': item.project.get('case').get('key'),
                    'value': item.project.get('case').get('value'),
                }
            },
            'status': item.status
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
            'id': item.uuid,
            'name': item.name,
            'tracker': {
                'issue': {
                    'id': item.issue_tracker.uuid,
                    'name': item.issue_tracker.name,
                },
                'case': {
                    'id': item.case_trakcer.uuid,
                    'name': item.case_trakcer.name,
                }
            },
            'project': {
                'issue': item.issue_tracker_project,
                'case': item.case_tracker_project,
            },
            'status': item.status
        }
    return project


@db_session
def add_project(item: dict):
    """
    Add Project
    :param item: {
        name: String,
        tracker: {
            issue: UUID,
            case: UUID
        },
        project: {
            issue: {
                key: String
                value: String
            },
            case: {
                key: String,
                value: String
            },
        }
    }
    :return:
    """
    _issue_tracker = get(p for p in Project if str(p.issue_tracker_id) == item.get('tracker').get('issue').get('id'))
    _issue_tracker = get(p for p in Project if str(p.issue_tracker_id) == item.get('tracker').get('issue').get('id'))
    _case_tracker = get(c for c in Tracker if str(c.uuid) == item.get('tracker').get('case').get('id'))
    _project = Project(
        name=item.get('name'),
        tracker=item.get('tracker').get('issue'),
        issue_tracker_project=item.get('project').get('issue'),
        case_tracker_id=item.get('tracker').get('case'),
        case_tracker_project=item.get('project').get('case')
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
    _project.name = item.get('name')
    _project.status = item.get('status') or 'active'
    _project.issue_tracker = get(c for c in Tracker if str(c.uuid) == item.get('tracker').get('issue').get('id'))
    _project.issue_tracker_project = item.get('project').get('issue')
    _project.case_tracker = get(c for c in Tracker if str(c.uuid) == item.get('tracker').get('case').get('id'))
    _project.case_tracker_project = item.get('project').get('case')
    return _project.uuid


@db_session
def set_project_status(project_id: dict, project_status: str):
    """
    Delete Project
    :param project_id:
    :param project_status:
    :return:
    """
    _project = get(p for p in Project if str(p.uuid) == project_id)
    _project.status = project_status.lower()
    return True


if __name__ == '__main__':
    print(u'This is a service of project')
