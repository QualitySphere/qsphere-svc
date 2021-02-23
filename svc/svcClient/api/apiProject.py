#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import svcProject
from utils.exceptionHandle import DefaultError


def list_project():
    """
    GET /api/projects
    :return:
    """
    try:
        return {
            'title': 'Succeed to List Project',
            'detail': svcProject.list_project()
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to List Project', detail=str(e))


def get_project(project_id):
    """
    GET /api/project/{project_id}
    :param project_id:
    :return:
    """
    try:
        return {
            'title': 'Succeed to Get Project',
            'detail': svcProject.get_project(project_id)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to Get Project', detail=str(e))


def add_project(body):
    """
    POST /api/projects
    :param body:
    :return:
    """
    try:
        return {
            'title': 'Succeed to Create Project',
            'detail': svcProject.add_project(body)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to Create Project', detail=str(e))


def update_project(project_id, body):
    """
    PUT /api/project/{project_id}
    :param project_id:
    :param body:
    :return:
    """
    try:
        return {
            'title': 'Succeed to Update Project',
            'detail': svcProject.update_project(project_id, body)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to Update Project', detail=str(e))


def update_project_status(project_id, body):
    """
    PUT /api/project/{project_id}/status
    :param project_id:
    :param body:
    :return:
    """
    try:
        return {
            'title': 'Succeed to change Project Status',
            'detail': svcProject.set_project_status(project_id, body)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to change Project Status', detail=str(e))


def delete_project(project_id):
    """
    DELETE /api/project/{project_id}
    :param project_id:
    :return:
    """
    try:
        svcProject.set_project_status(project_id, {'status': 'delete'})
        return {
            'title': 'Delete Project Succeed',
        }, 204
    except Exception as e:
        raise DefaultError(title='Delete Project Failed', detail=str(e))


if __name__ == '__main__':
    print('This is API for project')
