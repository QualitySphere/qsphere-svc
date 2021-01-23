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
        sprints = svcSprint.list_sprint(sprint_status=['active', 'disable'])
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


def add_sprint(body):
    """
    POST /api/sprint
    :param body:
    :return:
    """
    try:
        sprint_id = svcSprint.add_sprint(body)
        return {
            'title': 'Add Sprint Succeed',
            'detail': {
                'id': sprint_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Add Sprint Failed', detail=str(e))


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
                'id': sprint_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Update Sprint Failed', detail=str(e))


def update_sprint_status(sprint_id, body):
    pass


def delete_sprint(sprint_id):
    """
    DELETE /api/sprint/{sprint_id}
    :param sprint_id:
    :return:
    """
    try:
        svcSprint.set_sprint_status(sprint_id, sprint_status='delete')
        return {
            'title': 'Delete Sprint Succeed',
        }, 204
    except Exception as e:
        raise DefaultError(title='Delete Sprint Failed', detail=str(e))


def disable_sprint(sprint_id):
    """
    PUT /api/sprint/{sprint_id}/disable
    :param sprint_id:
    :return:
    """
    try:
        svcSprint.set_sprint_status(sprint_id, sprint_status='disable')
        return {
            'title': 'Disable Sprint Succeed',
        }, 204
    except Exception as e:
        raise DefaultError(title='Disable Sprint Failed', detail=str(e))


def active_sprint(sprint_id):
    """
    PUT /api/sprint/{sprint_id}/active
    :param sprint_id:
    :return:
    """
    try:
        svcSprint.set_sprint_status(sprint_id, sprint_status='active')
        return {
            'title': 'Active Sprint Succeed',
        }, 204
    except Exception as e:
        raise DefaultError(title='Active Sprint Failed', detail=str(e))
