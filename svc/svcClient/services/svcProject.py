#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pony.orm import db_session, select, get
from models.models import Tracker, Project


@db_session
def list_project():
    """
    List All Projects
    :return:[{
        'id': string,
        'name': string,
        'issue_tracker': {
            'tracker_name': string,
            'project_name': string,
        },
        'case_tracker': {
            'tracker_name': string,
            'project_name': string,
        },
        'status': string
    }]
    """
    items = list()
    for item in select(p for p in Project if p.status in ['active', 'disable']).order_by(Project.name):
        items.append({
            'id': item.uuid,
            'name': item.name,
            'issue_tracker': {
                'tracker_name': item.issue_tracker.name if item.issue_tracker else '',
                'project_name': item.issue_project.get('project_value')
            },
            'case_tracker': {
                'tracker_name': item.case_tracker.name if item.case_tracker else '',
                'project_name': item.case_project.get('project_value')
            },
            'status': item.status
        })
    return {
        'count': len(items),
        'results': items
    }


@db_session
def get_project(project_id: str):
    """
    Get Project
    :param project_id:
    :return: {
        'id': string,
        'name': string,
        'issue_tracker': {
            'tracker_id': string,
            'tracker_name': string,
            'project_key': string,
            'project_name': string,
        },
        'case_tracker': {
            'tracker_id': string,
            'tracker_name': string,
            'project_key': string,
            'project_name': string,
        },
        'status': string
    }
    """
    project = get(p for p in Project if str(p.uuid) == project_id)
    item = dict()
    if project:
        item = {
            'id': project.uuid,
            'name': project.name,
            'issue_tracker': {
                'tracker_id': project.issue_tracker.uuid if project.issue_tracker else '',
                'tracker_name': project.issue_tracker.name if project.issue_tracker else '',
                'project_key': project.issue_project.get('project_key'),
                'project_value': project.issue_project.get('project_value'),
            },
            'case_tracker': {
                'tracker_id': project.case_tracker.uuid if project.case_tracker else '',
                'tracker_name': project.case_tracker.name if project.case_tracker else '',
                'project_key': project.case_project.get('project_value'),
                'project_value': project.case_project.get('project_value'),
            },
            'status': project.status
        }
    return item


@db_session
def add_project(body: dict):
    """
    Add Project
    :param body: {
        'name': string,
        'issue_tracker': {
            'tracker_id': string,
            'project_key': string,
            'project_value': string,
        },
        'case_tracker': {
            'tracker_id': string,
            'project_key': string,
            'project_value': string
        }
    }
    :return: project_id
    """
    i_tracker = body.get('issue_tracker')
    c_tracker = body.get('case_tracker')
    project = Project(name=body.get('name'))
    if i_tracker.get('tracker_id'):
        project.issue_tracker = get(t for t in Tracker if str(t.uuid) == i_tracker.get('tracker_id'))
        project.issue_project = {
            'project_key': i_tracker.get('project_key'),
            'project_value': i_tracker.get('project_value')
        }
    if c_tracker.get('tracker_id'):
        project.case_tracker = get(t for t in Tracker if str(t.uuid) == c_tracker.get('tracker_id'))
        project.case_project = {
            'project_key': c_tracker.get('project_key'),
            'project_value': c_tracker.get('project_value')
        }
    return {
        'id': project.uuid,
        'name': project.name,
        'issue_tracker': {
            'tracker_id': project.issue_tracker.uuid if project.issue_tracker else '',
            'tracker_name': project.issue_tracker.name if project.issue_tracker else '',
            'project_key': project.issue_project.get('project_key'),
            'project_value': project.issue_project.get('project_value'),
        },
        'case_tracker': {
            'tracker_id': project.case_tracker.uuid if project.case_tracker else '',
            'tracker_name': project.case_tracker.name if project.case_tracker else '',
            'project_key': project.case_project.get('project_value'),
            'project_value': project.case_project.get('project_value'),
        },
        'status': project.status
    }


@db_session
def update_project(project_id: str, body: dict):
    """
    Update Project
    :param project_id:
    :param body: {
        'name': string,
        'issue_tracker': {
            'tracker_id': string,
            'project_key': string,
            'project_value': string,
        },
        'case_tracker': {
            'tracker_id': string,
            'project_key': string,
            'project_value': string
        }
    }
    :return:
    """
    i_tracker = body.get('issue_tracker')
    c_tracker = body.get('case_tracker')
    project = get(p for p in Project if str(p.uuid) == project_id)
    project.name = body.get('name')
    if i_tracker.get('tracker_id'):
        project.issue_tracker = get(t for t in Tracker if str(t.uuid) == i_tracker.get('tracker_id'))
        project.issue_project = {
            'project_key': i_tracker.get('project_key'),
            'project_value': i_tracker.get('project_value')
        }
    if c_tracker.get('tracker_id'):
        project.case_tracker = get(t for t in Tracker if str(t.uuid) == c_tracker.get('tracker_id'))
        project.case_project = {
            'tracker_id': c_tracker.get('tracker_id'),
            'project_key': c_tracker.get('project_key'),
            'project_value': c_tracker.get('project_value')
        }
    return {
        'id': project.uuid,
        'name': project.name,
        'issue_tracker': {
            'tracker_id': project.issue_tracker.uuid if project.issue_tracker else '',
            'tracker_name': project.issue_tracker.name if project.issue_tracker else '',
            'project_key': project.issue_project.get('project_key'),
            'project_value': project.issue_project.get('project_value'),
        },
        'case_tracker': {
            'tracker_id': project.case_tracker.uuid if project.case_tracker else '',
            'tracker_name': project.case_tracker.name if project.case_tracker else '',
            'project_key': project.case_project.get('project_value'),
            'project_value': project.case_project.get('project_value'),
        },
        'status': project.status
    }


@db_session
def set_project_status(project_id: dict, body: dict):
    """
    Change Project Status: active, disable, delete
    :param project_id:
    :param body: {
        'status': string
    }
    :return:
    """
    project = get(p for p in Project if str(p.uuid) == project_id)
    project.status = body.get('status').lower()
    return {
        'id': project.uuid,
        'status': project.status
    }


if __name__ == '__main__':
    print(u'This is SERVICE for project')
