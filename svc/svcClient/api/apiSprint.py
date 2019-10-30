#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import svcSprint
from utils.exceptionHandle import DefaultError


def list_sprint():
    """
    GET /api/sprint
    :return:
    """
    try:
        sprints = svcSprint.list_sprint()
        return {
            'title': 'List All Sprint Succeed',
            'detail': {
                'count': len(sprints),
                'results': sprints
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='List All Sprint Failed', detail=str(e))


def get_sprint(sprint_id):
    """
    GET /api/sprint/{sprint_id}
    :param sprint_id:
    :return:
    """
    try:
        sprint = svcSprint.get_sprint(sprint_id)
        return {
            'title': 'Get Sprint Succeed',
            'detail': sprint
        }, 200
    except Exception as e:
        raise DefaultError(title='Get Sprint Failed', detail=str(e))


def create_sprint(body):
    """
    POST /api/sprint
    :param body:
    :return:
    """
    try:
        sprint_id = svcSprint.create_sprint(body)
        return {
            'title': 'Create Sprint Succeed',
            'detail': {
                'sprint_id': sprint_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Create Sprint Failed', detail=str(e))


def update_sprint(sprint_id, body):
    """
    PUT /api/sprint/{sprint_id}
    :param sprint_id:
    :param body:
    :return:
    """
    try:
        svcSprint.update_sprint(sprint_id, body)
        return {
            'title': 'Update Sprint Succeed',
            'detail': {
                'sprint_id': sprint_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Update Sprint Failed', detail=str(e))


def delete_sprint(sprint_id):
    """
    DELETE /api/sprint/{sprint_id}
    :param sprint_id:
    :return:
    """
    try:
        svcSprint.delete_sprint(sprint_id)
        return {
            'title': 'Delete Sprint Succeed',
        }, 204
    except Exception as e:
        raise DefaultError(title='Delete Sprint Failed', detail=str(e))


def active_sprint(sprint_id, body):
    """
    PUT /api/sprint/{sprint_id}/active
    :param sprint_id:
    :param body:
    :return:
    """
    try:
        status = svcSprint.active_sprint(sprint_id, body.get('active'))
        return {
            'title': 'Change Sprint Active Status Succeed',
            'detail': {
                'active': status
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Change Sprint Active Status Failed', detail=str(e))


