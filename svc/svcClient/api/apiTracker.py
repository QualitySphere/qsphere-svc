#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import svcTracker
from utils.exceptionHandle import DefaultError


def get_tracker(tracker_id: str):
    """
    GET /api/tracker/{tracker_id}
    :param tracker_id:
    :return: {}
    """
    try:
        return {
            'title': 'Succeed to get Tracker',
            'detail': svcTracker.get_tracker(tracker_id)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to get Tracker', detail=str(e))


def add_tracker(body):
    """
    POST /api/trackers
    :param body:
    :return: {}
    """
    try:
        return {
            'title': 'Succeed to add Tracker',
            'detail': svcTracker.add_tracker(body)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to add Tracker', detail=str(e))


def update_tracker(tracker_id, body):
    """
    PUT /api/tracker/{tracker_id}
    :param tracker_id:
    :param body:
    :return: tracker_id
    """
    try:
        return {
            'title': 'Succeed to update Tracker',
            'detail': svcTracker.update_tracker(tracker_id, body)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to update Tracker', detail=str(e))


def update_tracker_status(tracker_id, body):
    """
    PUT /api/tracker/{tracker_id}/status
    :param tracker_id:
    :param body:
    :return:
    """
    try:
        return {
            'title': 'Succeed to change Tracker status',
            'detail': svcTracker.set_tracker_status(tracker_id, body)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to change Tracker status', detail=str(e))
    pass


def list_tracker():
    """
    GET /api/trackers
    :return: [{}]
    """
    try:
        return {
            'title': 'Succeed to list Tracker',
            'detail': svcTracker.list_tracker()
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to list Tracker', detail=str(e))


def delete_tracker(tracker_id):
    """
    DELETE /api/tracker/{tracker_id}
    :param tracker_id:
    :return:
    """
    try:
        svcTracker.set_tracker_status(tracker_id, {'status': 'delete'})
        return {
            'title': 'Succeed to delete Tracker'
        }, 204
    except Exception as e:
        raise DefaultError(title='Failed to delete Tracker', detail=str(e))


def list_tracker_project(tracker_id):
    """
    GET /api/tracker/{tracker_id}/projects
    :param tracker_id:
    :return:
    """
    try:
        return {
           'title': 'Succeed to list Project from Tracker',
           'detail': svcTracker.list_tracker_project(tracker_id)
       }, 200
    except Exception as e:
        raise DefaultError(title='Failed to list Project from Tracker', detail=str(e))


def list_tracker_sprint(tracker_id):
    """
    GET /api/tracker/{tracker_id}/sprints
    :param tracker_id:
    :return:
    """
    try:
        return {
            'title': 'Succeed to list Sprint from tracker',
            'detail': svcTracker.list_tracker_sprint(tracker_id)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to list Sprint from tracker', detail=str(e))


def list_tracker_issue_field(tracker_id):
    """
    GET /api/tracker/{tracker_id}/issue_fields
    :param tracker_id:
    :return:
    """
    try:
        return {
            'title': 'Succeed to list Issue Field from tracker',
            'detail': svcTracker.list_tracker_issue_field(tracker_id)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to list Issue Field from tracker', detail=str(e))


def list_tracker_issue_field_value(tracker_id: str, field: str, project=None):
    """
    GET /api/tracker/{tracker_id}/issue_field/{issue_field_id}
    :param tracker_id:
    :param field:
    :param project:
    :return:
    """
    try:
        return {
            'title': 'Succeed to list Issue Field Value from tracker',
            'detail': svcTracker.list_tracker_issue_field_value(
                tracker_id=tracker_id,
                project_key=project,
                field_key=field,
            )
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to list Issue Field Value from tracker', detail=str(e))


if __name__ == '__main__':
    print('This is API for tracker')
