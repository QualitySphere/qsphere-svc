#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from jira import JIRA
import connexion
from flask import current_app


class JiraIssue(object):
    def __init__(self, server, user, password):
        self._client = JIRA(server=server, basic_auth=(user, password))

    def _close(self):
        self._client.close()

    def _search(self, jql: str):
        current_app.logger.info(u'Search: %s' % jql)
        return self._client.search_issues(jql_str=jql)

    def sync(self, jql: str):
        current_app.logger.info(u'')
        self._search(jql)


if __name__ == '__main__':
    print(u'This is a service of JIRA issue')
