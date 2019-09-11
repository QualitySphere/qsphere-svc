#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from flask import current_app
from pony.orm import db_session, select, get
from models.models import Connection, Project, Sprint
from clientJira.utils.jiraClient import JiraSession
from threading import Thread


def _get_issue_project_status(server, account, password, project):
    # 从数据库中的 issue sprint 表中获取每个 project 的最后一次数据
    # with db_session:
    #     select(_sprints  _sprints )
    # _issue_types = ', '.join(sprint.issue_types)
    pass


# def _get_jira(issues, key1, key2, value):
#     with JiraSession(server, account, password) as jira_session:
#     issues[key1] = dict()
#     issue_sprint_issues[key1][str(key2)] = jira_session.search_issues(value).get('total')


def _search_issues(server, account, password, key_jql, value_jql, issues):
    with JiraSession(server, account, password) as jira_session:
        issues[str(key_jql)] = jira_session.search_issues(value_jql).get('total')
    return True


@db_session
def _get_issue_sprint_status(sprint_id):
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    server = sprint.project.connection.server
    account = sprint.project.connection.account
    password = sprint.project.connection.password
    jqls = sprint.queries.get('jqls')
    issues = dict()
    threads = list()
    for key, value in jqls.items():
        issues[key] = dict()
        for key_jql, value_jql in value.items():
            threads.append(
                Thread(
                    target=_search_issues,
                    args=(server, account, password, key_jql, value_jql, issues[key])
                )
            )
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    for key, value in jqls.items():
        issues[key]['total'] = sum(issues[key].values())
    # 额外对 categories 的数据进行处理
    categories = issues['categories']
    # others 中存放的实际是 total 的值
    categories['total'] = categories['others']
    categories['others'] = categories['total'] - categories['regression'] - categories['previous'] - categories['newfeature']
    return issues


def get_sprint_issues(sprint_id):
    detail = _get_issue_sprint_status(sprint_id)
    return {
        'status': 200,
        'title': 'Succeed To Get Sprint Issues',
        'detail': detail
    }, 200


def sync_jira_data():
    pass


if __name__ == '__main__':
    print(u'This is a service of JIRA issue')
