#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pony.orm import db_session, get, select
from models.models import Tracker, Project
from utils.jiraClient import JiraSession


@db_session
def get_tracker(tracker_id: str):
    """
    Get Tracker
    :param tracker_id:
    :return: {
        'id': UUID,
        'name': string,
        'type': string,
        'info': dict,
        'status': string
    }
    """
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
    if not item:
        raise Exception('Wrong Tracker ID')
    return {
        'id': item.uuid,
        'name': item.name,
        'type': item.type,
        'info': item.info,
        'status': item.status,
    }


@db_session
def add_tracker(body: dict):
    """
    Add Tracker
    :param body: {
        'name': string,
        'type': string,
        'info': {
            'host': string,
            'account': string,
        },
        'token': string
    }
    :return: tracker_id
    """
    if body.get('type').lower() == 'jira':
        with JiraSession(
            body.get('info').get('host'),
            body.get('info').get('account'),
            body.get('token')
        ) as jira_session:
            assert body.get('info').get('account') == jira_session.get_user()
    else:
        raise Exception('ONLY support JIRA')
    item = Tracker(
        name=body.get('name'),
        type=body.get('type'),
        info={
            'host': body.get('info').get('host'),
            'account': body.get('info').get('account'),
        },
        token=body.get('token')
    )
    return {
        'id': item.uuid,
        'name': item.name,
        'type': item.type,
        'info': item.info,
        'status': item.status
    }


@db_session
def update_tracker(tracker_id: str, body: dict):
    """
    Update Tracker Info
    :param tracker_id:
    :param body: {
        'name': string,
        'type': string,
        'info': {
            'host': string,
            'account': string,
        },
        'token': string
    }
    :return: {}
    """
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
    if not item:
        raise Exception('Wrong Tracker ID')
    if body.get('type').lower() == 'jira':
        with JiraSession(
            body.get('info').get('host'),
            body.get('info').get('account'),
            body.get('token')
        ) as jira_session:
            assert body.get('info').get('account') == jira_session.get_user()
    else:
        raise Exception('ONLY support JIRA')
    item.name = body.get('name'),
    item.type = body.get('type'),
    item.info = {
        'host': body.get('info').get('host'),
        'account': body.get('info').get('account'),
    },
    item.token = body.get('token')
    return {
        'id': item.uuid,
        'name': item.name,
        'type': item.type,
        'info': item.info,
        'status': item.status
    }


@db_session
def set_tracker_status(tracker_id: str, body: dict):
    """
    Set Tracker Status as active, disable or delete
    :param tracker_id:
    :param body: {
        'status': 'delete' | 'active' | 'disable'
    }
    :return: {}
    """
    if body.get('status').lower() not in ['active', 'disable', 'delete']:
        raise Exception('Unknown tracker status: %s' % body.get('status'))
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
    if not item:
        raise Exception('Wrong Tracker ID')
    item.status = body.get('status').lower()
    return {
        'id': item.uuid,
        'status': item.status
    }


@db_session
def list_tracker():
    """
    List All Tracker Info
    :return: [{}]
    """
    items = list()
    for item in select(t for t in Tracker if t.status in ['active', 'disable']):
        items.append({
            'id': item.uuid,
            'name': item.name,
            'type': item.type,
            'info': item.info,
            'status': item.status,
        })
    return {
        'count': len(items),
        'results': items
    }


@db_session
def list_tracker_project(tracker_id: str):
    """
    List projects from tracker server
    :param tracker_id:
    :return: [{}]
    """
    tracker = get(t for t in Tracker if str(t.uuid) == tracker_id)
    projects = list()
    if tracker.type == 'jira':
        with JiraSession(
            tracker.info.get('host'),
            tracker.info.get('account'),
            tracker.token
        ) as jira_session:
            for p in jira_session.get_projects():
                projects.append({
                    'key': p.id,
                    'value': p.name
                })
    else:
        raise Exception('ONLY support JIRA')
    return {
        'count': len(projects),
        'results': projects
    }


@db_session
def list_tracker_sprint(tracker_id: str):
    """
    List sprints from tracker server
    :param tracker_id:
    :return: [{}]
    """
    tracker = get(t for t in Tracker if str(t.uuid) == tracker_id)
    sprints = list()
    if tracker.type == 'jira':
        with JiraSession(
                tracker.info.get('host'),
                tracker.info.get('account'),
                tracker.token
        ) as jira_session:
            for s in jira_session.get_sprints():
                sprints.append({
                    'key': s.id,
                    'value': s.name
                })
    else:
        raise Exception('ONLY support JIRA')
    return {
        'count': len(sprints),
        'results': sprints
    }


@db_session
def list_tracker_issue_field(tracker_id: str):
    """
    List issue fields from tracker server
    :param tracker_id:
    :return: [{}]
    """
    tracker = get(t for t in Tracker if str(t.uuid) == tracker_id)
    fields = list()
    if tracker.type == 'jira':
        with JiraSession(
                tracker.info.get('host'),
                tracker.info.get('account'),
                tracker.token
        ) as jira_session:
            for f in jira_session.get_issue_fields():
                fields.append({
                    'key': f['id'],
                    'value': f['name']
                })
    else:
        raise Exception('ONLY support JIRA')
    return {
        'count': len(fields),
        'results': fields
    }


@db_session
def list_tracker_issue_field_value(tracker_id: str, field_key: str, project_key=None):
    """
    List issue field values in the project from tracker server
    :param tracker_id:
    :param field_key:
    :param project_key:
    :return:
    """
    tracker = get(t for t in Tracker if str(t.uuid) == tracker_id)
    values = list()
    items = list()
    if tracker.type == 'jira':
        with JiraSession(
                tracker.info.get('host'),
                tracker.info.get('account'),
                tracker.token
        ) as jira_session:
            if field_key == 'status':
                items = jira_session.get_issue_statuses()
            elif field_key == 'issuetype':
                items = jira_session.get_issue_types()
            elif field_key == 'versions':
                if project_key:
                    items = jira_session.get_project_versions(pid=project_key)
                else:
                    raise Exception('project is required')
        for item in items:
            values.append({
                'key': item.id,
                'value': item.name
            })
    else:
        raise Exception('ONLY support JIRA')
    return {
        'count': len(values),
        'results': values
    }


if __name__ == '__main__':
    print(u'This is SERVICE for tracker')
