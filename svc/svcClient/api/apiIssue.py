#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from services import svcIssue
from utils.exceptionHandle import DefaultError


def sync_issue_data(sprint_id=None):
    """
    GET /api/issue/sync
    :param sprint_id:
    :return:
    """
    try:
        svcIssue.sync_issue_data(sprint_id)
        return {
            'title': 'Succeed to Sync Issue Data',
        }, 200
        # if sprint_id:
        #     svcIssue.sync_sprint_issue_data(sprint_id)
        #     return {
        #         'title': 'Sync Sprint Issue Succeed',
        #     }, 200
        # else:
        #     svcIssue.sync_issue_data()
        #     return {
        #         'title': 'Sync All Sprints Issue Succeed',
        #     }, 200
    except Exception as e:
        raise DefaultError(title='Failed to Sync Issue Data', detail=str(e))


def get_issue_status(sprint_id=None):
    """
    GET /api/issue/status
    :param sprint_id:
    :return:
    """
    try:
        return {
            'title': 'Succeed to get Sprints Bug Status',
            'detail': svcIssue.get_issue_status(sprint_id)
        }, 200
        # bugs = svcIssue.get_active_sprint_issue_status()
        # return {
        #     'title': 'Get All Active Sprints Bug Status Succeed',
        #     'detail': bugs
        # }, 200
    except Exception as e:
        raise DefaultError(title='Failed to get Sprints Bug Status', detail=str(e))


if __name__ == '__main__':
    print(u'This is API of issue')
