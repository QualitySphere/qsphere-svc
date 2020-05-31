#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import svcIssue
from utils.exceptionHandle import DefaultError


def sync_issue(sprint_id=None):
    """
    GET /api/issue/sync
    :return:
    """
    try:
        if sprint_id:
            svcIssue.sync_sprint_issue_data(sprint_id)
            return {
                       'title': 'Sync Sprint Issue Succeed',
                   }, 200
        else:
            svcIssue.sync_issue_data()
            return {
                       'title': 'Sync All Sprints Issue Succeed',
                   }, 200
    except Exception as e:
        raise DefaultError(title='Sync Sprint Issue Failed', detail=str(e))


def get_active_sprint_issue_status():
    """
    GET /api/issue/status
    :return:
    """
    try:
        bugs = svcIssue.get_active_sprint_issue_status()
        return {
            'title': 'Get All Active Sprints Bug Status Succeed',
            'detail': bugs
        }, 200
    except Exception as e:
        raise DefaultError(title='Get All Active Sprints Bug Status Failed', detail=str(e))
