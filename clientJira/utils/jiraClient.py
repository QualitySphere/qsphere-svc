#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from jira import JIRA
import connexion
from flask import current_app
from pony.orm import *


class JiraSession(object):
    def __init__(self, server, account, password):
        self.server = server
        self.account = account
        self.password = password
        self.jira_session = JIRA(server=self.server, basic_auth=(self.account, self.password))

    def __enter__(self):
        assert self.jira_session.current_user() == self.account
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.jira_session.close()

    def search_issues(self, jql):
        current_app.logger.info(u'JIRA Search: %s' % jql)
        return self.jira_session.search_issues(jql_str=jql, maxResults=128, json_result=True)

    def get_projects(self):
        current_app.logger.info(u'Get JIRA Projects')
        return self.jira_session.projects()

    def get_user(self):
        current_app.logger.info(u'Get JIRA Current User')
        return self.jira_session.current_user()


if __name__ == '__main__':
    print(u'This is a service of JIRA connection')
