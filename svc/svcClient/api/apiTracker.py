#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import svcTracker
from utils.exceptionHandle import DefaultError


def get_tracker(tracker_id: str):
    """
    GET /api/tracker/{tracker_id}
    :param tracker_id:
    :return:
    """
    try:
        tracker = svcTracker.get_tracker(tracker_id)
        return {
            'title': 'Get Tracker Succeed',
            'detail': tracker
        }, 200
    except Exception as e:
        raise DefaultError(title='Get Tracker Succeed', detail=str(e))


def add_tracker(body):
    """
    POST /api/tracker
    :param body:
    :return:
    """
    _name = body.get('name')
    _type = body.get('type')
    _info = body.get('info')
    _secret = body.get('secret')
    try:
        tracker_id = svcTracker.add_tracker(tracker_name=_name,
                                            tracker_type=_type,
                                            tracker_info=_info,
                                            tracker_secret=_secret)
        return {
            'title': 'Add Tracker Succeed',
            'detail': {
                'id': tracker_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Create Tracker Failed', detail=str(e))


def update_tracker(tracker_id, body):
    """
    PUT /api/tracker/{tracker_id}
    :param tracker_id:
    :param body:
    :return:
    """
    _name = body.get('name')
    _type = body.get('type')
    _info = body.get('info')
    _secret = body.get('secret')
    try:
        tracker_id = svcTracker.update_tracker(tracker_id=tracker_id,
                                               tracker_name=_name,
                                               tracker_type=_type,
                                               tracker_info=_info,
                                               tracker_secret=_secret)
        return {
            'title': 'Update Tracker Succeed',
            'detail': {
                'id': tracker_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Update Connection Failed', detail=str(e))


def list_tracker():
    """
    GET /api/tracker
    :return:
    """
    try:
        trackers = svcTracker.list_tracker(tracker_status=['active', 'disable'])
        return {
            'title': 'List Tracker Succeed',
            'detail': {
                'count': len(trackers),
                'results': trackers
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='List Tracker Failed', detail=str(e))


def delete_tracker(tracker_id):
    """
    DELETE /api/tracker/{tracker_id}
    :param tracker_id:
    :return:
    """
    try:
        svcTracker.set_tracker_status(tracker_id, 'delete')
        return {
            'title': 'Delete Tracker Succeed'
        }, 204
    except Exception as e:
        raise DefaultError(title='Delete Tracker Failed', detail=str(e))


def active_tracker(tracker_id):
    """
    PUT /api/tracker/{tracker_id}/active
    :param tracker_id:
    :return:
    """
    try:
        svcTracker.set_tracker_status(tracker_id, 'active')
        return {
            'title': 'Active Tracker Succeed'
        }, 200
    except Exception as e:
        raise DefaultError(title='Active Tracker Failed', detail=str(e))


def disable_tracker(tracker_id):
    """
    PUT /api/tracker/{tracker_id}/disable
    :param tracker_id:
    :return:
    """
    try:
        svcTracker.set_tracker_status(tracker_id, 'disable')
        return {
            'title': 'Disable Tracker Succeed'
        }, 200
    except Exception as e:
        raise DefaultError(title='Disable Tracker Failed', detail=str(e))


def list_tracker_project(tracker_id):
    """
    GET /api/tracker/{tracker_id}/project
    :param tracker_id:
    :return: {key: value}
    """
    try:
        projects = svcTracker.list_tracker_project(tracker_id)
        return {
                   'title': 'List Project From Tracker Succeed',
                   'detail': {
                       'count': len(projects),
                       'results': projects
                   }
               }, 200
    except Exception as e:
        raise DefaultError(title='List Project From Tracker Failed', detail=str(e))


def list_tracker_issue_type(tracker_id):
    """
    GET /api/tracker/{tracker_id}/issue_types
    :param tracker_id:
    :return: {key: value}
    """
    try:
        types = svcTracker.list_tracker_issue_type(tracker_id)
        return {
                   'title': 'List Issue Types From Tracker Succeed',
                   'detail': {
                       'count': len(types),
                       'results': types
                   }
               }, 200
    except Exception as e:
        raise DefaultError(title='List Issue Types From Tracker Failed', detail=str(e))


def list_tracker_issue_status(tracker_id):
    """
    GET /api/tracker/{tracker_id}/issue_statuses
    :param tracker_id:
    :return: {key: value}
    """
    try:
        statuses = svcTracker.list_tracker_issue_status(tracker_id)
        return {
                   'title': 'List Issue Statuses From Tracker Succeed',
                   'detail': {
                       'count': len(statuses),
                       'results': statuses
                   }
            }, 200
    except Exception as e:
        raise DefaultError(title='List Issue Statuses From Tracker Failed', detail=str(e))
