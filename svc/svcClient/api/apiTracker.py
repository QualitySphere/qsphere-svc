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
        tracker = svcTracker.get_tracker(tracker_id)
        return {
            'title': 'Succeed to get Tracker',
            'detail': tracker
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to get Tracker', detail=str(e))


def add_tracker(body):
    """
    POST /api/trackers
    :param body:
    :return: tracker_id
    """
    try:
        tracker_id = svcTracker.add_tracker(
            tracker_name=body.get('name'),
            tracker_type=body.get('type'),
            tracker_info=body.get('info'),
            tracker_token=body.get('token')
        )
        return {
            'title': 'Succeed to add Tracker',
            'detail': {
                'id': tracker_id
            }
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
        tracker_id = svcTracker.update_tracker(
            tracker_id=tracker_id,
            tracker_name=body.get('name'),
            tracker_type=body.get('type'),
            tracker_info=body.get('info'),
            tracker_token=body.get('token')
        )
        return {
            'title': 'Succeed to update Tracker',
            'detail': {
                'id': tracker_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to update Tracker', detail=str(e))


def update_tracker_status(tracker_id, status):
    """
    PUT /api/tracker/{tracker_id}/status
    :param tracker_id:
    :param status:
    :return:
    """
    try:
        tracker_status = svcTracker.set_tracker_status(
            tracker_id=tracker_id,
            tracker_status=status
        )
        return {
            'title': 'Succeed to change Tracker status',
            'detail': tracker_status
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
        trackers = svcTracker.list_tracker(
            tracker_status=['active', 'disable']
        )
        return {
            'title': 'Succeed to list Tracker',
            'detail': {
                'count': len(trackers),
                'results': trackers
            }
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
        svcTracker.set_tracker_status(
            tracker_id=tracker_id,
            tracker_status='delete'
        )
        return {
            'title': 'Succeed to delete Tracker'
        }, 204
    except Exception as e:
        raise DefaultError(title='Failed to delete Tracker', detail=str(e))


# def active_tracker(tracker_id):
#     """
#     PUT /api/tracker/{tracker_id}/active
#     :param tracker_id:
#     :return:
#     """
#     try:
#         svcTracker.set_tracker_status(tracker_id, 'active')
#         return {
#             'title': 'Active Tracker Succeed'
#         }, 200
#     except Exception as e:
#         raise DefaultError(title='Active Tracker Failed', detail=str(e))


# def disable_tracker(tracker_id):
#     """
#     PUT /api/tracker/{tracker_id}/disable
#     :param tracker_id:
#     :return:
#     """
#     try:
#         svcTracker.set_tracker_status(tracker_id, 'disable')
#         return {
#             'title': 'Disable Tracker Succeed'
#         }, 200
#     except Exception as e:
#         raise DefaultError(title='Disable Tracker Failed', detail=str(e))


def list_tracker_project(tracker_id):
    """
    GET /api/tracker/{tracker_id}/project
    :param tracker_id:
    :return: [{'key': '', 'value': ''}]
    """
    try:
        projects = svcTracker.list_tracker_project(tracker_id)
        return {
           'title': 'Succeed to list Project from Tracker',
           'detail': {
               'count': len(projects),
               'results': projects
           }
       }, 200
    except Exception as e:
        raise DefaultError(title='Failed to list Project from Tracker', detail=str(e))


# def list_tracker_issue_type(tracker_id):
#     """
#     GET /api/tracker/{tracker_id}/issue_types
#     :param tracker_id:
#     :return: [{'key': '', 'value': ''}]
#     """
#     try:
#         types = svcTracker.list_tracker_issue_type(tracker_id)
#         return {
#                    'title': 'List Issue Types From Tracker Succeed',
#                    'detail': {
#                        'count': len(types),
#                        'results': types
#                    }
#                }, 200
#     except Exception as e:
#         raise DefaultError(title='List Issue Types From Tracker Failed', detail=str(e))
#
#
# def list_tracker_issue_status(tracker_id):
#     """
#     GET /api/tracker/{tracker_id}/issue_statuses
#     :param tracker_id:
#     :return: [{'key': '', 'value': ''}]
#     """
#     try:
#         statuses = svcTracker.list_tracker_issue_status(tracker_id)
#         return {
#                    'title': 'List Issue Statuses From Tracker Succeed',
#                    'detail': {
#                        'count': len(statuses),
#                        'results': statuses
#                    }
#             }, 200
#     except Exception as e:
#         raise DefaultError(title='List Issue Statuses From Tracker Failed', detail=str(e))


def list_tracker_sprint(tracker_id):
    """
    GET /api/tracker/{tracker_id}/sprint
    :param tracker_id:
    :return: [{'key': '', 'value': ''}]
    """
    try:
        sprints = svcTracker.list_tracker_sprint(
            tracker_id=tracker_id
        )
        return {
            'title': 'Succeed to list Sprint from tracker',
            'detail': {
                'count': len(sprints),
                'results': sprints
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to list Sprint from tracker', detail=str(e))


def list_tracker_issue_field(tracker_id):
    """
    GET /api/tracker/{tracker_id}/issue_field
    :param tracker_id:
    :return: [{'key': '', 'value': ''}]
    """
    try:
        fields = svcTracker.list_tracker_issue_field(
            tracker_id=tracker_id
        )
        return {
            'title': 'Succeed to list Issue Field from tracker',
            'detail': {
                'count': len(fields),
                'results': fields
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to list Issue Field from tracker', detail=str(e))


def list_tracker_issue_field_value(tracker_id, issue_field_id, project_id):
    """
    GET /api/tracker/{tracker_id}/issue_field/{issue_field_id}
    :param tracker_id:
    :param issue_field_id:
    :param project_id:
    :return: [{'key': '', 'value': ''}]
    """
    try:
        values = svcTracker.list_tracker_issue_field_value(
            tracker_id=tracker_id,
            project_id=project_id,
            field_key=issue_field_id,
        )
        return {
            'title': 'Succeed to list Issue Field Value from tracker',
            'detail': {
                'count': len(values),
                'results': values
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to list Issue Field Value from tracker', detail=str(e))

