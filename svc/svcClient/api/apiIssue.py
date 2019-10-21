#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import svcIssue
from utils.exceptionHandle import DefaultError


def sync_sprint_issue(sprint_id):
    """
    GET /api/issue/{sprint_id}/sync
    :param sprint_id:
    :return:
    """
    try:
        svcIssue.sync_sprint_issue_data(sprint_id)
        return {
            'title': 'Sync Sprint Issue Succeed',
        }, 200
    except Exception as e:
        raise DefaultError(title='Sync Sprint Issue Failed', detail=str(e))


def sync_issue():
    """
    GET /api/issue/sync
    :return:
    """
    try:
        svcIssue.sync_issue_data()
        return {
            'title': 'Sync All Sprints Issue Succeed',
        }, 200
    except Exception as e:
        raise DefaultError(title='Sync All Sprints Issue Failed', detail=str(e))
