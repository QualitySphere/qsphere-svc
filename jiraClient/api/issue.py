#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from jiraClient.services.issue import JiraIssue


def sync(body):
    _server = body.get('jiraServer')
    _user = body.get('jiraUser')
    _password = body.get('jiraPassword')
    _issue = JiraIssue(server=_server, user=_user, password=_password)
    return _issue.sync('')
