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
from models.models import Tracker
from utils.jiraClient import JiraSession


@db_session
def add_tracker(tracker_name: str, tracker_type: str, tracker_info: dict, tracker_secret: str):
    """
    Add Tracker
    :param tracker_name:
    :param tracker_type: jira
    :param tracker_info:
    :param tracker_secret:
    :return: tracker_id
    """
    if tracker_type.lower() == 'jira':
        with JiraSession(
                tracker_info.get('host'),
                tracker_info.get('account'),
                tracker_secret) as jira_session:
            assert tracker_info.get('account') == jira_session.get_user()
    else:
        raise Exception('Only support JIRA')
    tracker = Tracker(
        name=tracker_name,
        type=tracker_type,
        info=tracker_info,
        secret=tracker_secret
    )
    return tracker.uuid


@db_session
def update_tracker(tracker_id: str, tracker_name: str, tracker_type: str, tracker_info: dict, tracker_secret: str):
    """
    Update Tracker Info
    :param tracker_id:
    :param tracker_name:
    :param tracker_type: jira
    :param tracker_info:
    :param tracker_secret:
    :return: tracker_id
    """
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
    if item:
        if tracker_type.lower() == 'jira':
            with JiraSession(
                    tracker_info.get('host'),
                    tracker_info.get('account'),
                    tracker_secret) as jira_session:
                assert tracker_info.get('account') == jira_session.get_user()
        else:
            raise Exception('Only support JIRA')
        item.name = tracker_name
        item.type = tracker_type
        item.info = tracker_info
        item.secret = tracker_secret
    return item.uuid


@db_session
def list_tracker(tracker_status=None):
    """
    List All Tracker Info
    :param tracker_status:
    :return: tracker list
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
    :return: None or tracker info
    """
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
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
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
    if item:
        item.status = tracker_status.lower()
    return item.uuid


@db_session
def list_tracker_project(tracker_id: str):
    """
    List projects from tracker server
    :param tracker_id:
    :return:
    """
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
    projects = list()
    if item.type == 'jira':
        with JiraSession(
                item.info.get('host'),
                item.info.get('account'),
                item.secret) as jira_session:
            for p in jira_session.get_projects():
                projects.append({
                    'key': p.key,
                    'value': p.name
                })
    return projects


@db_session
def list_tracker_issue_type(tracker_id: str):
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
    issue_types = list()
    if item.type == 'jira':
        with JiraSession(
                item.info.get('host'),
                item.info.get('account'),
                item.secret) as jira_session:
            for t in jira_session.get_issue_types():
                issue_types.append({
                    'key': t.id,
                    'value': t.name
                })
    return issue_types


@db_session
def list_tracker_issue_status(tracker_id: str):
    item = get(t for t in Tracker if str(t.uuid) == tracker_id)
    issue_statuses = list()
    if item.type == 'jira':
        with JiraSession(
                item.info.get('host'),
                item.info.get('account'),
                item.secret) as jira_session:
            for s in jira_session.get_issue_statuses():
                issue_statuses.append({
                    'key': s.id,
                    'value': s.name
                })
    return issue_statuses


if __name__ == '__main__':
    print(u'This is a service of tracker')
