#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from flask import current_app
from pony.orm import db_session, select, get
from models.models import Connection, Project, Sprint, IssueProject, IssueSprint, IssueFeature
from clientJira.utils.jiraClient import JiraSession
from threading import Thread
from datetime import datetime
import logging


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


def debug_function(sprint_id):
    # DEBUG Start
    # 获取 sprint 信息
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    server = sprint.project.connection.server
    account = sprint.project.connection.account
    password = sprint.project.connection.password
    jqls = sprint.queries.get('jqls')
    # 登录 JIRA 用 JQL 查询数据
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
    # 额外对 categories 的数据进行处理, others 中存放的实际是 total 的值
    categories = issues['categories']
    categories['total'] = categories['others']
    categories['others'] = categories['total'] - categories['regression'] - categories['previous'] - categories[
        'newfeature']
    return issues


@db_session
def get_issues(sprint_id):
    # project issues status
    # sprint issues status
    # feature issues status
    issues = debug_function(sprint_id)
    return {
        'title': 'Succeed To Get Issues',
        'detail': issues
    }, 200


def _search_issues(server, account, password, key_jql, value_jql, issues):
    with JiraSession(server, account, password) as jira_session:
        issues[str(key_jql)] = jira_session.search_issues(value_jql).get('total')
    return True


@db_session
def _get_jira_issues(sprint_id):
    capture_time = datetime.utcnow()
    # 获取 sprint 信息
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    server = sprint.project.connection.server
    account = sprint.project.connection.account
    password = sprint.project.connection.password
    jqls = sprint.queries.get('jqls')
    # 登录 JIRA 用 JQL 查询数据
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
    # 额外对 categories 的数据进行处理, others 中存放的实际是 total 的值
    categories = issues['categories']
    categories['total'] = categories['others']
    categories['others'] = categories['total'] - categories['regression'] - categories['previous'] - categories['newfeature']
    logging.debug(issues)
    # 更新数据库
    logging.info('Start to update DB for project issues status')
    issue_project = get(p for p in IssueProject if str(p.sprint.uuid) == sprint_id)
    if issue_project:
        issue_project.capture_at = capture_time
        issue_project.categories = issues.get('categories')
        issue_project.found_since = issues.get('issue_found_since')
    else:
        IssueProject(
            capture_at=capture_time,
            sprint=sprint,
            categories=issues.get('categories'),
            found_since=issues.get('issue_found_since')
        )
    logging.info('Complete update')
    logging.info('Start to update DB for sprint issues status')
    # issue_sprint = get(s for s in IssueSprint if str(s.sprint.uuid) == sprint_id)
    # if issue_sprint:
    #     issue_sprint.capture_at = capture_time
    #     issue_sprint.status = issues.get('overall')
    #     issue_sprint.categories = issues.get('categories')
    #     issue_sprint.found_since = issues.get('issue_found_since')
    #     issue_sprint.found_in_rcs = issues.get('rcs')
    # else:
    IssueSprint(
        capture_at=capture_time,
        sprint=sprint,
        status=issues.get('overall'),
        categories=issues.get('categories'),
        found_since=issues.get('issue_found_since'),
        found_in_rcs=issues.get('rcs')
    )
    logging.info('Complete update')
    logging.info('Start to update DB for feature issues status')
    for key in issues.keys():
        if key not in ['overall', 'categories', 'rcs', 'issue_found_since']:
            # issue_feature = get(f for f in IssueFeature if str(f.sprint.uuid) == sprint_id and f.name == key)
            # if issue_feature:
            #     issue_feature.capture_at = capture_time
            #     issue_feature.status = issues.get(key)
            # else:
            IssueFeature(
                capture_at=capture_time,
                sprint=sprint,
                name=key,
                status=issues.get(key)
            )
    logging.info('Complete update')
    return issues


def sync_jira_data(sprint_id):
    try:
        _get_jira_issues(sprint_id)
        return {
            'title': 'Succeed To Sync Issues From JIRA'
        }, 200
    except Exception as e:
        logging.error(e)
        return {
            'title': 'Failed to sync data from JIRA',
            'detail': str(e)
        }, 400


if __name__ == '__main__':
    print(u'This is a service of JIRA issue')
