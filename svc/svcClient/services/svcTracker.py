#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Tracker Model
# uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
# name = Required(str)
# type = Required(str)
# info = Optional(Json)  # JIRA: {host: '', account: ''}
# secret = Optional(str)  # JIRA: 'password'
# status = Required(str, default='active')  # active, disable, delete


from pony.orm import db_session, get, select
from models.models import Tracker, Project
from utils.jiraClient import JiraSession


@db_session
def add_tracker(
        tracker_name: str,
        tracker_type: str,
        tracker_info: dict,
        tracker_token: str
):
    """
    Add Tracker
    :param tracker_name:
    :param tracker_type: jira
    :param tracker_info:
    :param tracker_token:
    :return: tracker_id
    """
    if tracker_type.lower() == 'jira':
        with JiraSession(
                tracker_info.get('host'),
                tracker_info.get('account'),
                tracker_token) as jira_session:
            assert tracker_info.get('account') == jira_session.get_user()
    else:
        raise Exception('Only support JIRA')
    tracker = Tracker(
        name=tracker_name,
        type=tracker_type,
        info=tracker_info,
        token=tracker_token
    )
    return tracker.uuid


@db_session
def update_tracker(
        tracker_id: str,
        tracker_name: str,
        tracker_type: str,
        tracker_info: dict,
        tracker_token: str
):
    """
    Update Tracker Info
    :param tracker_id:
    :param tracker_name:
    :param tracker_type: jira
    :param tracker_info:
    :param tracker_token:
    :return: tracker_id
    """
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
    if not item:
        raise Exception('Wrong Tracker ID')
    if tracker_type.lower() == 'jira':
        with JiraSession(tracker_info.get('host'), tracker_info.get('account'), tracker_token) as jira_session:
            assert tracker_info.get('account') == jira_session.get_user()
    else:
        raise Exception('ONLY support JIRA')
    item.name = tracker_name
    item.type = tracker_type
    item.info = tracker_info
    item.token = tracker_token
    return item.uuid


@db_session
def list_tracker(tracker_status=None):
    """
    List All Tracker Info
    :param tracker_status:
    :return: [{
        'id': UUID,
        'name': string,
        'type': string,
        'info': dict,
        'status': string
    }]
    """
    trackers = list()
    if tracker_status:
        items = select(t for t in Tracker if t.status in tracker_status)
    else:
        items = select(t for t in Tracker)
    for item in items:
        trackers.append({
            'id': item.uuid,
            'name': item.name,
            'type': item.type,
            'info': item.info,
            'status': item.status,
        })
    return trackers


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
def set_tracker_status(tracker_id: str, tracker_status: str):
    """
    Set Tracker Status as active, disable or delete
    :param tracker_id:
    :param tracker_status: delete, active, disable
    :return: {
        'id': UUID,
        'status': 'string'
    }
    """
    if tracker_status.lower() not in ['active', 'disable', 'delete']:
        raise Exception('Unknown tracker status: %s' % tracker_status)
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
    if not item:
        raise Exception('Wrong Tracker ID')
    item.status = tracker_status.lower()
    return {
        'id': item.uuid,
        'status': item.status
    }


@db_session
def list_tracker_project(tracker_id: str):
    """
    List projects from tracker server
    :param tracker_id:
    :return: [{
        'key': string,
        'value': string
    }]
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
    return projects


def list_tracker_sprint(tracker_id: str):
    """
    List sprints from tracker server
    :param tracker_id:
    :return: [{
        'key': string,
        'value': string
    }]
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
    return sprints


def list_tracker_issue_field(tracker_id: str):
    """
    List issue fields from tracker server
    :param tracker_id:
    :return: [{
        'key': string,
        'value': string
    }]
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
    return fields


def list_tracker_issue_field_value(tracker_id: str, project_id: str, field_key: str):
    values = list()
    items = list()
    tracker = get(t for t in Tracker if str(t.uuid) == tracker_id)
    project = get(p for p in Project if str(p.uuid) == project_id)
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
                items = jira_session.get_project_versions(pid=project.issue_tracker['project_key'])
            for item in items:
                values.append({
                    'key': item.id,
                    'value': item.name
                })
    else:
        raise Exception('ONLY support JIRA')
    return values


if __name__ == '__main__':
    print(u'This is a service of tracker')
