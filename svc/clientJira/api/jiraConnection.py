#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from clientJira.services import jiraConnection


def health_check():
    return {
        'Status': 'Healthy'
    }, 200


def get_connection():
    return jiraConnection.get_connection()


def post_connection(body):
    return jiraConnection.create_connection(body)


def put_connection(body):
    return jiraConnection.update_connection(body)


def delete_connection():
    pass

