#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Tracker Model
# uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
# name = Required(str)
# type = Required(str)
# info = Optional(Json)  # JIRA: {host: '', account: '', password: ''}
# status = Required(str, default='active')  # active, disable, delete


from pony.orm import db_session, get, select
from models.models import Tracker
from utils.jiraClient import JiraSession


@db_session
def add_tracker(tracker_name: str, tracker_type: str, tracker_info: dict):
    """
    Add Tracker
    :param tracker_name:
    :param tracker_type: jira
    :param tracker_info:
    :return: tracker_id
    """
    if tracker_type.lower() == 'jira':
        with JiraSession(
                tracker_info.get('host'),
                tracker_info.get('account'),
                tracker_info.get('password')) as jira_session:
            assert tracker_info.get('account') == jira_session.get_user()
    else:
        raise Exception('Only support JIRA')
    tracker = Tracker(
        name=tracker_name,
        type=tracker_type,
        info=tracker_info
    )
    return tracker.uuid


@db_session
def update_tracker(tracker_id: str, tracker_name: str, tracker_type: str, tracker_info: dict):
    """
    Update Tracker Info
    :param tracker_id:
    :param tracker_name:
    :param tracker_type: jira
    :param tracker_info:
    :return: tracker_id
    """
    item = get(c for c in Tracker if str(c.uuid) == tracker_id)
    if item:
        if tracker_type.lower() == 'jira':
            with JiraSession(
                    tracker_info.get('host'),
                    tracker_info.get('account'),
                    tracker_info.get('password')) as jira_session:
                assert tracker_info.get('account') == jira_session.get_user()
        else:
            raise Exception('Only support JIRA')
        item.name = tracker_name
        item.type = tracker_type
        item.info = tracker_info
    return item.uuid


@db_session
def list_tracker(tracker_status=None):
    """
    List All Tracker Info
    :param tracker_status:
    :return: tracker list
    """
    if tracker_status:
        items = select(c for c in Tracker if c.status == tracker_status)
    else:
        items = select(c for c in Tracker)
    trackers = list()
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
    :return: None or tracker info
    """
    item = get(c for c in Tracker if str(c.uuid) == tracker_id)
    tracker = dict()
    if item:
        tracker = {
            'id': item.uuid,
            'name': item.name,
            'type': item.type,
            'info': item.info,
            'status': item.status,
        }
    return tracker


@db_session
def set_tracker_status(tracker_id: str, tracker_status: str):
    """
    Set Tracker Status as active, disable or delete
    :param tracker_id:
    :param tracker_status: delete, active, disable
    :return: tracker_id
    """
    item = get(c for c in Tracker if str(c.uuid) == tracker_id)
    if item:
        item.status = tracker_status.lower()
    return item.uuid


@db_session
def list_tracker_project(tracker_id: str):
    item = get(c for c in Tracker if str(c.uuid) == tracker_id)
    projects = list()
    if item.type == 'jira':
        with JiraSession(
                item.get('info').get('host'),
                item.get('info').get('account'),
                item.get('info').get('password')) as jira_session:
            for p in jira_session.get_projects():
                projects.append({
                    'key': p.key,
                    'value': p.name
                })
    return projects


@db_session
def list_tracker_issue_type(tracker_id: str):
    item = get(c for c in Tracker if str(c.uuid) == tracker_id)
    issue_types = list()
    if item.type == 'jira':
        with JiraSession(
                item.get('info').get('host'),
                item.get('info').get('account'),
                item.get('info').get('password')) as jira_session:
            for t in jira_session.get_issue_types():
                issue_types.append({
                    'key': t.id,
                    'value': t.name
                })
    return issue_types


@db_session
def list_tracker_issue_status(tracker_id: str):
    item = get(c for c in Tracker if str(c.uuid) == tracker_id)
    issue_statuses = list()
    if item.type == 'jira':
        with JiraSession(
                item.get('info').get('host'),
                item.get('info').get('account'),
                item.get('info').get('password')) as jira_session:
            for s in jira_session.get_issue_statuses():
                issue_statuses.append({
                    'key': s.id,
                    'value': s.name
                })
    return issue_statuses


if __name__ == '__main__':
    print(u'This is a service of tracker')
