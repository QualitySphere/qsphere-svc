#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from clientJira.services import jiraIssue


def get_project_issues():
    pass


def get_sprint_issues(sprint_id):
    return jiraIssue.get_sprint_issues(sprint_id)
