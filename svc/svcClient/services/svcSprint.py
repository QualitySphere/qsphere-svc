#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pony.orm import db_session, select, get
from models.models import Project, Sprint
import logging


@db_session
def list_sprint(sprint_status=None):
    """
    List ALl Sprints
    :return:
    """
    items = select(s for s in Sprint if s.active != 'delete').order_by(Sprint.name)
    sprints = list()
    for item in items:
        logging.info('Get sprint %s[%s] info' % (item.uuid, item.name))
        sprints.append({
            'project_id': item.project.uuid,
            'project_name': item.project.name,
            'sprint_id': item.uuid,
            'sprint_name': item.name,
            'active': item.active
        })
    return sprints


@db_session
def get_sprint(sprint_id: str):
    """
    Get Sprint
    :param sprint_id:
    :return:
    """
    item = get(s for s in Sprint if str(s.uuid) == sprint_id)
    sprint_info = dict()
    if item:
        sprint_info = {
            "project_id": item.project.uuid,
            "project_name": item.project.name,
            "sprint_id": item.uuid,
            "sprint_name": item.name,
            "product_version": item.version,
            "features": item.features,
            "rcs": item.rcs,
            "issue_found_since": item.issue_found_since,
            "issue_types": item.issue_types,
            "issue_status": item.issue_status,
            "issue_categories": item.issue_categories,
            'jqls': item.queries.get('jqls'),
            'active': item.active
        }
    return sprint_info


@db_session
def active_sprint(sprint_id: str, active: str):
    """
    Change Sprint Active Status: enable/disable
    :param sprint_id:
    :param active:
    :return:
    """
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    sprint.active = active
    return sprint.active


@db_session
def delete_sprint(sprint_id: str):
    """
    Delete Sprint
    :param sprint_id:
    :return:
    """
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    sprint.active = 'delete'
    return True


def _generate_jqls(project_name, sprint_info: dict):
    """
    Internal Function: Generate JQL for Sprint
    :param project_name:
    :param sprint_info:
    :return:
    """
    jqls = {
        'overall': dict(),
        'categories': dict(),
        'rcs': dict(),
        'issue_found_since': dict(),
    }

    # 定义customer bug jql, 它不应该局限在 sprint 过程
    jqls['issue_found_since']['customer'] = ' AND '.join([
        'project = "%s"' % project_name,
        'issuetype in (%s)' % ', '.join(sprint_info.get('issue_types')),
        'labels = "%s"' % sprint_info.get('product_version'),
        'labels = "Customer"',
        ])

    # 定义 jql base, 用于后面的所有 jql
    jql_base = ' AND '.join([
        'project = "%s"' % project_name,
        'issuetype in (%s)' % ', '.join(sprint_info.get('issue_types')),
        'Sprint = "%s"' % sprint_info.get('sprint_name'),
        'labels = "%s"' % sprint_info.get('product_version'),
    ])

    logging.info('Generate JQL for overall')
    for k, v in sprint_info.get('issue_status').items():
        jqls['overall'][k] = ' AND '.join([
            jql_base,
            'status in (%s)' % ', '.join(v)
        ])

    logging.info('Generate JQL for features')
    for feature in sprint_info.get('features'):
        jql_feature_base = ' AND '.join([
            jql_base,
            'labels = "%s"' % feature,
        ])
        jqls[feature] = dict()
        for k, v in sprint_info.get('issue_status').items():
            jqls[feature][k] = ' AND '.join([
                jql_feature_base,
                'status in (%s)' % ', '.join(v)
            ])

    logging.info('Generate JQL for categories')
    if sprint_info.get('issue_categories') is None:
        sprint_info['issue_categories'] = ['Regression', 'Previous', 'NewFeature', 'Others']
    for category in sprint_info.get('issue_categories'):
        # Others 的类别将在下面进行处理
        if category == 'Others':
            continue
        jql_category = ' AND '.join([
            jql_base,
            'labels = "%s"' % category,
        ])
        jqls['categories'][category.lower()] = jql_category
    # Others 是除了 Regression, Previous, NewFeature 的类别
    # 实际中可能没有标记，这里不做jql不带任何相关标记，先获取总数，用于后面函数处理时候计算得出 others
    jqls['categories']['others'] = jql_base

    logging.info('Generate JQL for rcs')
    for rc in sprint_info.get('rcs'):
        jql_rc = ' AND '.join([
            jql_base,
            'labels = "%s"' % rc,
        ])
        jqls['rcs'][rc] = jql_rc

    logging.info('Generate JQL for issue found since')
    if sprint_info.get('issue_found_since') is None:
        sprint_info['issue_found_since'] = ['RegressionImprove', 'QAMissed', 'NewFeature', 'Customer']
    for since in sprint_info.get('issue_found_since'):
        # 来自 customer 的缺陷已经在一开始就生成了 jql，所以这里跳过
        if since == 'Customer':
            continue
        jql_issue_found_since = ' AND '.join([
            jql_base,
            'labels = "%s"' % since,
        ])
        jqls['issue_found_since'][since.lower()] = jql_issue_found_since
    logging.info('Complete to generate all JQLs')
    return jqls


@db_session
def create_sprint(sprint_info: dict):
    """
    Create Sprint
    :param sprint_info:
    :return:
    """
    _project = get(p for p in Project if str(p.uuid) == sprint_info.get('project_id'))
    _sprint = Sprint(
        project=_project,
        name=sprint_info.get('sprint_name'),
        version=sprint_info.get('product_version'),
        issue_types=sprint_info.get('issue_types'),
        features=sprint_info.get('features'),
        rcs=sprint_info.get('rcs'),
        issue_found_since=sprint_info.get('issue_status'),
        issue_status=sprint_info.get('issue_status'),
        issue_categories=sprint_info.get('issue_categories')
    )
    if _sprint.project.connection.issue_server.get('type') == 'jira':
        _sprint.queries = {
            'jqls': _generate_jqls(_project.name, sprint_info)
        }
    return _sprint.uuid


@db_session
def update_sprint(sprint_id: str, sprint_info: dict):
    """
    Update Sprint
    :param sprint_id:
    :param sprint_info:
    :return:
    """
    _project = get(p for p in Project if str(p.uuid) == sprint_info.get('project_id'))
    _sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    _sprint.project = _project
    _sprint.name = sprint_info.get('sprint_name')
    _sprint.version = sprint_info.get('product_version')
    _sprint.features = sprint_info.get('features')
    _sprint.rcs = sprint_info.get('rcs')
    _sprint.issue_types = sprint_info.get('issue_types')
    _sprint.issue_status = sprint_info.get('issue_status')
    _sprint.issue_categories = sprint_info.get('issue_categories')

    if _sprint.project.connection.issue_server.get('type') == 'jira':
        _sprint.queries = {
            'jqls': _generate_jqls(_project.name, sprint_info)
        }
    return _sprint.uuid


if __name__ == '__main__':
    print(u'This is a service of sprint')
