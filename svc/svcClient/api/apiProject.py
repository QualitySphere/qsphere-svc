#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import svcProject
from utils.exceptionHandle import DefaultError


def list_project():
    """
    GET /api/project
    :return:
    """
    try:
        projects = svcProject.list_project()
        return {
            'title': 'List Projects Succeed',
            'detail': {
                'count': len(projects),
                'results': projects
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='List Projects Failed', detail=str(e))


def get_project(project_id):
    """
    GET /api/project/{project_id}
    :param project_id:
    :return:
    """
    try:
        project = svcProject.get_project(project_id)
        return {
            'title': 'Get Project Succeed',
            'detail': project
        }, 200
    except Exception as e:
        raise DefaultError(title='Get Project Failed', detail=str(e))


def add_project(body):
    """
    POST /api/project
    :param body:
    :return:
    """
    try:
        project_id = svcProject.add_project(body)
        return {
            'title': 'Create Project Succeed',
            'detail': {
                'project_id': project_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Create Project Failed', detail=str(e))


def update_project(project_id, body):
    """
    PUT /api/project/{project_id}
    :param project_id:
    :param body:
    :return:
    """
    try:
        svcProject.update_project(project_id, body)
        return {
            'title': 'Update Project Succeed',
            'detail': {
                'project_id': project_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Update Project Failed', detail=str(e))


def delete_project(project_id):
    """
    DELETE /api/project/{project_id}
    :param project_id:
    :return:
    """
    try:
        svcProject.set_project_status(project_id, 'delete')
        return {
            'title': 'Delete Project Succeed',
        }, 204
    except Exception as e:
        raise DefaultError(title='Delete Project Failed', detail=str(e))


def disable_project(project_id):
    """
    PUT /api/project/{project_id}/disable
    :param project_id:
    :return:
    """
    try:
        svcProject.set_project_status(project_id, 'disable')
        return {
                   'title': 'Disable Project Succeed',
               }, 204
    except Exception as e:
        raise DefaultError(title='Disable Project Failed', detail=str(e))


def active_project(project_id):
    """
    PUT /api/project/{project_id}/active
    :param project_id:
    :return:
    """
    try:
        svcProject.set_project_status(project_id, 'active')
        return {
                   'title': 'Active Project Succeed',
               }, 204
    except Exception as e:
        raise DefaultError(title='Active Project Failed', detail=str(e))
