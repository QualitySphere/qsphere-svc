#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pony.orm import db_session, select, get
from models.models import *
from utils.jiraClient import JiraSession
from threading import Thread
from datetime import datetime
import logging


def _search_jira_issues(server, account, password, key_jql, value_jql, issues):
    """
    INTERNAL FUNCTION: Search JIRA Issues
    :param server: JIRA server
    :param account: JIRA account
    :param password: JIRA password
    :param key_jql: Key
    :param value_jql: JIRA JQL
    :param issues: issues
    :return:
    """
    with JiraSession(server, account, password) as jira_session:
        issues[str(key_jql)] = jira_session.search_issues(value_jql).get('total')
    return True


@db_session
def _sync_jira_data_for_sprint_all_issue(sprint_id: str):
    """
    INTERNAL FUNCTION: Sync Sprint All Issues From JIRA Server
    :param sprint_id:
    :return:
    """
    capture_time = datetime.utcnow()

    # 获取 sprint 信息
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    _issue_tracker = get(t for t in Tracker if t.uuid == sprint.project.tracker['issue']['id'])
    server = _issue_tracker.info.get('host')
    account = _issue_tracker.info.get('account')
    password = _issue_tracker.secret
    jqls = sprint.queries['issue']['jira']

    # 多线程登录 JIRA 用 JQL 收集所有数据
    issues = dict()
    threads = list()
    for key, value in jqls.items():
        issues[key] = dict()
        for key_jql, value_jql in value.items():
            threads.append(
                Thread(
                    target=_search_jira_issues,
                    args=(server, account, password, key_jql, value_jql, issues[key])
                )
            )
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    # 所有的数据组都计算出各自的 total 值
    for key, value in jqls.items():
        issues[key]['total'] = sum(issues[key].values())

    # 额外对 categories 的数据进行处理, others 中存放的实际是 total 的值
    # 因此真正的 others 是需要除去 regression,previous, newfeature
    categories = issues['categories']
    categories['total'] = categories['others']
    categories['others'] = categories['total'] - categories['regression'] - categories['previous'] - categories['newfeature']
    logging.debug(issues)

    # 生成一条新的数据记录
    logging.info('Start to update DB for sprint issues status')
    IssueSprint(
        capture_time=capture_time,
        sprint=sprint,
        status=issues.get('overall'),
        categories=issues.get('categories'),
        found_since=issues.get('issue_found_since'),
        found_in_rcs=issues.get('rcs')
    )
    logging.info('Complete update')

    # 更新 issue_sprint_latest 表中的迭代维度最新 RC 数据
    for rc_key, rc_value in issues.get('rcs').items():
        if rc_key == 'total':
            continue
        logging.info('Start to update DB for latest sprint issues status')
        issue_sprint = get(s for s in IssueSprintLatest if str(s.sprint.uuid) == sprint_id and s.rc == rc_key)
        if issue_sprint:
            issue_sprint.capture_time = capture_time
            issue_sprint.sprint = sprint
            issue_sprint.rc = rc_key
            issue_sprint.count = rc_value
        else:
            IssueSprintLatest(
                capture_time=capture_time,
                sprint=sprint,
                rc=rc_key,
                count=rc_value
            )
        logging.info('Complete update')

    # 更新 issue_project_latest 表中的项目维度最新数据
    logging.info('Start to update DB for latest project issues status')
    issue_project = get(p for p in IssueProjectLatest if str(p.sprint.uuid) == sprint_id)
    if issue_project:
        issue_project.capture_time = capture_time
        issue_project.categories = issues.get('categories')
        issue_project.found_since = issues.get('issue_found_since')
    else:
        IssueProjectLatest(
            capture_time =capture_time,
            sprint=sprint,
            categories=issues.get('categories'),
            found_since=issues.get('issue_found_since')
        )
    logging.info('Complete update')

    # 更新 issue_customer_latest 表中的项目维度客户反馈缺陷最新数据
    logging.info('Start to update DB for latest customer issues status')
    issue_customer = get(c for c in IssueCustomerLatest if str(c.sprint.uuid) == sprint_id)
    if issue_customer:
        issue_customer.capture_time = capture_time
        issue_customer.count = issues.get('issue_found_since').get('customer')
    else:
        IssueCustomerLatest(
            capture_time=capture_time,
            sprint=sprint,
            count=issues.get('issue_found_since').get('customer')
        )
    logging.info('Complete update')

    for key in issues.keys():
        if key in ['overall', 'categories', 'rcs', 'issue_found_since']:
            continue
        # 更新 issue_req 表中的功能数据
        logging.info('Start to update DB for requirement issues status')
        IssueReq(
            capture_time=capture_time,
            sprint=sprint,
            name=key,
            status=issues.get(key)
        )
        logging.info('Complete update')

        # 更新 issue_req_latest 表中的迭代维度的最新功能数据
        logging.info('Start to update DB for latest requirement issues status')
        issue_req = get(f for f in IssueReqLatest
                            if str(f.sprint.uuid) == sprint_id and f.name == key)
        if issue_req:
            issue_req.capture_time = capture_time
            issue_req.status = issues.get(key)
        else:
            IssueReqLatest(
                capture_time=capture_time,
                sprint=sprint,
                name=key,
                status=issues.get(key)
            )
        logging.info('Complete update')

    return True


@db_session
def _sync_jira_data_for_sprint_customer_issue(sprint_id: str):
    """
    INTERNAL FUNCTION: Sync Sprint Customer Issue From JIRA Server
    :param sprint_id:
    :return:
    """
    capture_time = datetime.utcnow()

    # 获取 sprint, connection 以及 bug from customer 的 JQL
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    _issue_tracker = get(t for t in Tracker if t.uuid == sprint.project.tracker['issue']['id'])
    server = _issue_tracker.info.get('host')
    account = _issue_tracker.info.get('account')
    password = _issue_tracker.secret
    jql = sprint.queries['issue']['jira'].get('issue_found_since').get('customer')

    # JQL 从 JIRA 中获取查询结果数量
    with JiraSession(server, account, password) as jira_session:
        count = jira_session.search_issues(jql).get('total')

    # 更新 issue_customer_latest 表中的项目维度客户反馈缺陷最新数据
    logging.info('Start to update DB for latest customer issues status')
    issue_customer = get(c for c in IssueCustomerLatest if str(c.sprint.uuid) == sprint_id)
    if issue_customer:
        issue_customer.capture_time = capture_time
        issue_customer.count = count
    else:
        IssueCustomerLatest(
            capture_time=capture_time,
            sprint=sprint,
            count=count
        )
    logging.info('Complete update')

    return True


@db_session
def sync_sprint_issue_data(sprint_id: str):
    """
    Sync Sprint Issue Data
    :param sprint_id:
    :return:
    """
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    _issue_tracker = get(t for t in Tracker if t.uuid == sprint.project.tracker['issue']['id'])
    if sprint.status == 'active':
        if _issue_tracker.type == 'jira':
            _sync_jira_data_for_sprint_all_issue(sprint_id)
    elif sprint.status == 'disable':
        if _issue_tracker.type == 'jira':
            _sync_jira_data_for_sprint_customer_issue(sprint_id)


@db_session
def sync_issue_data():
    """
    Sync All Sprints Issue Data
    :return:
    """
    # 同步数据库中所有存在的迭代
    sprints = select(s for s in Sprint if s.status != 'delete')
    threads = list()
    for sprint in sprints:
        logging.info('Start to sync data for sprint %s' % sprint.name)
        threads.append(
            Thread(
                target=sync_sprint_issue_data,
                args=(str(sprint.uuid),)
            )
        )
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    return True


@db_session
def get_active_sprint_issue_status():
    sprints = select(s for s in Sprint if s.status == 'active')
    items = list()
    bugs = list()
    for sprint in sprints:
        items.append(select(i for i in IssueSprint if i.sprint.uuid == sprint.uuid)
                     .order_by(IssueSprint.capture_time)
                     .first())
    for item in items:
        bugs.append({
            'sprint_name': item.sprint.name,
            'issue_status': item.status,
        })
    return bugs


def sync_sprint_case_data(sprint_id: str):
    """
    Sync Sprint Case Data
    :param sprint_id:
    :return:
    """
    pass


def sync_case_data():
    """
    Sync All Sprint Case Data
    :return:
    """
    pass


if __name__ == '__main__':
    print(u'This is a service of issue')
