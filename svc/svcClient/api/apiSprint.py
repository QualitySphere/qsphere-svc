#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import svcSprint
from utils.exceptionHandle import DefaultError


def list_sprint():
    """
    GET /api/sprints
    :return:
    """
    try:
        return {
            'title': 'Succeed to List All Sprint',
            'detail': svcSprint.list_sprint()
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to List All Sprint', detail=str(e))


def get_sprint(sprint_id):
    """
    GET /api/sprint/{sprint_id}
    :param sprint_id:
    :return:
    """
    try:
        return {
            'title': 'Succeed to Get Sprint',
            'detail': svcSprint.get_sprint(sprint_id)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to Get Sprint', detail=str(e))


def add_sprint(body):
    """
    POST /api/sprints
    :param body:
    :return:
    """
    try:
        return {
            'title': 'Succeed to Add Sprint',
            'detail': svcSprint.add_sprint(body)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to Add Sprint', detail=str(e))


def update_sprint(sprint_id, body):
    """
    PUT /api/sprint/{sprint_id}
    :param sprint_id:
    :param body:
    :return:
    """
    try:
        return {
            'title': 'Succeed to Update Sprint',
            'detail': svcSprint.update_sprint(sprint_id, body)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to Update Sprint', detail=str(e))


def update_sprint_status(sprint_id, body):
    """
    PUT /api/sprint/{sprint_id}/status
    :param sprint_id:
    :param body: {
        'status': 'active',  # 'disable', 'active'
    }
    :return:
    """
    try:
        return {
            'title': 'Succeed to Change Sprint Status',
            'detail': svcSprint.set_sprint_status(sprint_id, body)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to Change Sprint Status', detail=str(e))


def delete_sprint(sprint_id):
    """
    DELETE /api/sprint/{sprint_id}
    :param sprint_id:
    :return:
    """
    try:
        svcSprint.set_sprint_status(sprint_id, {'status': 'delete'})
        return {
            'title': 'Delete Sprint Succeed',
        }, 204
    except Exception as e:
        raise DefaultError(title='Delete Sprint Failed', detail=str(e))


if __name__ == '__main__':
    print(u'This is API of sprint')
