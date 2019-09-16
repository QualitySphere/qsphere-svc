#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from clientJira.services import jiraIssue


# def get_project_issues():
#     pass


def get_issues(sprint_id):
    return jiraIssue.get_issues(sprint_id)


def sync_issues(sprint_id):
    return jiraIssue.sync_jira_data(sprint_id)
