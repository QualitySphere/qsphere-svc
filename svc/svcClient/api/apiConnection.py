#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import svcConnection
from utils.exceptionHandle import DefaultError


def get_connection(connection_id: str):
    """
    GET /api/connection/{connection_id}
    :param connection_id:
    :return:
    """
    try:
        connection = svcConnection.get_connection(connection_id)
        return {
            'title': 'Get Connection Succeed',
            'detail': connection
        }, 200
    except Exception as e:
        raise DefaultError(title='Get Connection Succeed', detail=str(e))


def create_connection(body):
    """
    POST /api/connection
    :param body:
    :return:
    """
    try:
        connection_id = svcConnection.create_connection(body)
        return {
            'title': 'Create Connection Succeed',
            'detail': {
                'connection_id': connection_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Create Connection Failed', detail=str(e))


def update_connection(connection_id, body):
    """
    PUT /api/connection/{connection_id}
    :param connection_id:
    :param body:
    :return:
    """
    try:
        connection_id = svcConnection.update_connection(connection_id, body)
        return {
            'title': 'Update Connection Succeed',
            'detail': {
                'connection_id': connection_id
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='Update Connection Failed', detail=str(e))


def list_connection():
    """
    GET /api/connection
    :return:
    """
    try:
        connections = svcConnection.list_connection()
        return {
            'title': 'List Connection Succeed',
            'detail': {
                'count': len(connections),
                'results': connections
            }
        }, 200
    except Exception as e:
        raise DefaultError(title='List Connection Failed', detail=str(e))


def delete_connection(connection_id):
    """
    DELETE /api/connection/{connection_id}
    :param connection_id:
    :return:
    """
    try:
        svcConnection.delete_connection(connection_id)
        return {
            'title': 'Delete Connection Succeed'
        }, 204
    except Exception as e:
        raise DefaultError(title='Delete Connection Failed', detail=str(e))

