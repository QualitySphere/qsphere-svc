#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from flask import current_app
from pony.orm import db_session, select, get
from models.models import *
from clientJira.utils.jiraClient import JiraSession
from threading import Thread
from datetime import datetime
import logging


@db_session
def get_issues(sprint_id):
    # feature issues status
    sprint_issue = select(s for s in IssueSprint
                          if str(s.sprint.uuid) == sprint_id).order_by(IssueSprint.capture_at).first()
    feature_issue = select(f for f in IssueFeatureLatest
                           if str(f.sprint.uuid) == sprint_id)
    if sprint_issue:
        detail = {
                'sprint_id': sprint_issue.sprint.uuid,
                'status': sprint_issue.status,
                'categories': sprint_issue.categories,
                'found_since': sprint_issue.found_since,
                'found_in_rcs': sprint_issue.found_in_rcs,
                'features': dict()
        }
        for fi in feature_issue:
            detail['features'][fi.name] = fi.status
        return {
            'title': 'Succeed To Get Issues',
            'detail': detail
        }, 200
    else:
        return {
            'title': 'No Issues',
        }, 404


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
    logging.info('Start to update DB for sprint issues status')
    IssueSprint(
        capture_at=capture_time,
        sprint=sprint,
        status=issues.get('overall'),
        categories=issues.get('categories'),
        found_since=issues.get('issue_found_since'),
        found_in_rcs=issues.get('rcs')
    )
    logging.info('Complete update')

    for rc_key, rc_value in issues.get('rcs').items():
        if rc_key == 'total':
            continue
        logging.info('Start to update DB for latest sprint issues status')
        issue_sprint = get(s for s in IssueSprintLatest if str(s.sprint.uuid) == sprint_id and s.rc == rc_key)
        if issue_sprint:
            issue_sprint.capture_at = capture_time
            issue_sprint.sprint = sprint
            issue_sprint.rc = rc_key
            issue_sprint.count = rc_value
        else:
            IssueSprintLatest(
                capture_at=capture_time,
                sprint=sprint,
                rc=rc_key,
                count=rc_value
            )
        logging.info('Complete update')

    logging.info('Start to update DB for latest project issues status')
    issue_project = get(p for p in IssueProjectLatest if str(p.sprint.uuid) == sprint_id)
    if issue_project:
        issue_project.capture_at = capture_time
        issue_project.categories = issues.get('categories')
        issue_project.found_since = issues.get('issue_found_since')
    else:
        IssueProjectLatest(
            capture_at=capture_time,
            sprint=sprint,
            categories=issues.get('categories'),
            found_since=issues.get('issue_found_since')
        )
    logging.info('Complete update')

    for key in issues.keys():
        if key not in ['overall', 'categories', 'rcs', 'issue_found_since']:
            logging.info('Start to update DB for feature issues status')
            IssueFeature(
                capture_at=capture_time,
                sprint=sprint,
                name=key,
                status=issues.get(key)
            )
            logging.info('Complete update')

            logging.info('Start to update DB for latest feature issues status')
            issue_feature = get(f for f in IssueFeatureLatest
                                if str(f.sprint.uuid) == sprint_id and f.name == key)
            if issue_feature:
                issue_feature.capture_at = capture_time
                issue_feature.status = issues.get(key)
            else:
                IssueFeatureLatest(
                    capture_at=capture_time,
                    sprint=sprint,
                    name=key,
                    status=issues.get(key)
                )
            logging.info('Complete update')

    return issues


def sync_jira_sprint_data(sprint_id):
    try:
        _get_jira_issues(sprint_id)
        return {
            'title': 'Succeed To Sync Sprint %s Issues From JIRA' % sprint_id
        }, 200
    except Exception as e:
        logging.error(e)
        return {
            'title': 'Failed To Sync Sprint %s Issues from JIRA' % sprint_id,
            'detail': str(e)
        }, 400


@db_session
def sync_jira_data():
    sprints = select(s for s in Sprint if s.active == 'enable').order_by(Sprint.name)
    if sprints:
        try:
            threads = list()
            for sprint in sprints:
                threads.append(
                    Thread(
                        target=_get_jira_issues,
                        args=(str(sprint.uuid),)
                    )
                )
            for t in threads:
                t.setDaemon(True)
                t.start()
            for t in threads:
                t.join()
            return {
                'title': 'Succeed To Sync All Sprints Issues From JIRA'
            }, 200
        except Exception as e:
            return {
                'title': 'Failed To Sync Issues From JIRA: %s' % e,
            }, 400
    else:
        return {
            'title': 'No Sprint Need To Sync'
        }, 200


if __name__ == '__main__':
    print(u'This is a service of JIRA issue')
