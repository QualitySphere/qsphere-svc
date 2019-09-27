#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import connexion
from flask import current_app
from pony.orm import db_session, select, get
from models.models import Connection, Project, Sprint
from clientJira.utils.jiraClient import JiraSession
import logging


@db_session
def list_sprints():
    items = select(s for s in Sprint if s.active == 'enable').order_by(Sprint.name)
    if items:
        logging.info('List %s sprints from DB' % items.count())
        sprints = list()
        for item in items:
            logging.info('Get sprint %s[%s] info' % (item.uuid, item.name))
            sprints.append({
                'sprint_id': item.uuid,
                'sprint_name': item.name
            })
        return {
            'title': 'Succeed To List Sprint',
            'detail': {
                'count': items.count(),
                'results': sprints
            }
        }, 200
    else:
        logging.info('No sprint in DB')
        return {
            'title': 'Sprint Not Found',
        }, 404


def get_sprint(sprint_id: str):
    with db_session:
        item = get(
            _sprint for _sprint in Sprint if
            str(_sprint.uuid) == sprint_id
        )
    if item:
        return {
            'title': 'Succeed To Get Sprint',
            'detail': {
                "sprint_name": item.name,
                "product_version": item.version,
                "features": item.features,
                "rcs": item.rcs,
                "issue_found_since": item.issue_found_since,
                "issue_types": item.issue_types,
                "issue_status": item.issue_status,
                "issue_categories": item.issue_categories,
                'jqls': item.queries.get('jqls'),
            }
        }, 200
    else:
        return {
            'title': 'Sprint Not Found'
        }, 404


def active_sprint(sprint_id: str):
    with db_session:
        item = get(s for s in Sprint if str(s.uuid) == sprint_id)
        item.active = 'active'
    return {
        'title': 'Succeed To Active Sprint'
    }, 204


def disable_sprint(sprint_id: str):
    with db_session:
        item = get(s for s in Sprint if str(s.uuid) == sprint_id)
        item.active = 'disable'
    return {
        'title': 'Succeed To Disable Sprint'
    }, 204


def delete_sprint(sprint_id: str):
    with db_session:
        item = get(s for s in Sprint if str(s.uuid) == sprint_id)
        item.active = 'delete'
    return {
        'title': 'Succeed To Delete Sprint'
    }, 204


def _generate_jqls(sprint: dict):
    jqls = {
        'overall': dict(),
        'categories': dict(),
        'rcs': dict(),
        'issue_found_since': dict(),
    }

    jql_base = ' AND '.join([
        'project = %s' % sprint.get('sprint_name'),
        'issuetype in (%s)' % ', '.join(sprint.get('issue_types')),
        'Sprint = "%s"' % sprint.get('sprint_name'),
    ])

    logging.info('Generate JQL for overall')
    for k, v in sprint.get('issue_status').items():
        jqls['overall'][k] = ' AND '.join([
            jql_base,
            'status in (%s)' % ', '.join(v)
        ])

    logging.info('Generate JQL for features')
    for feature in sprint.get('features'):
        jql_feature_base = ' AND '.join([
            jql_base,
            'labels = "%s"' % sprint.get('product_version'),
            'labels = "%s"' % feature,
        ])
        jqls[feature] = dict()
        for k, v in sprint.get('issue_status').items():
            jqls[feature][k] = ' AND '.join([
                jql_feature_base,
                'status in (%s)' % ', '.join(v)
            ])

    logging.info('Generate JQL for categories')
    if sprint.get('issue_categories') is None:
        sprint['issue_categories'] = ['regression', 'previous', 'newfeature', 'others']
    for category in sprint.get('issue_categories'):
        jql_category = ' AND '.join([
            jql_base,
            'labels = "%s"' % sprint.get('product_version'),
            'labels = "%s"' % category,
        ])
        jqls['categories'][category] = jql_category
    jqls['categories']['others'] = ' AND '.join([
        jql_base,
        'labels = "%s"' % sprint.get('product_version'),
    ])

    logging.info('Generate JQL for rcs')
    for rc in sprint.get('rcs'):
        jql_rc = ' AND '.join([
            jql_base,
            'labels = "%s"' % rc,
        ])
        jqls['rcs'][rc] = jql_rc

    logging.info('Generate JQL for issue found since')
    if sprint.get('issue_found_since') is None:
        sprint['issue_found_since'] = ['regression_improve', 'qa_missed', 'new_feature', 'customer']
    for since in sprint.get('issue_found_since'):
        jql_issue_found_since = ' AND '.join([
            jql_base,
            'labels = "%s"' % since,
        ])
        jqls['issue_found_since'][since] = jql_issue_found_since
    logging.info('Complete to generate all JQLs')
    return jqls


def create_sprint(sprint: dict):
    with db_session:
        _project = get(p for p in Project if str(p.uuid) == sprint.get('project_id'))
        _sprint = Sprint(
            project=_project,
            name=sprint.get('sprint_name'),
            version=sprint.get('product_version'),
            features=sprint.get('features'),
            rcs=sprint.get('rcs'),
            issue_types=sprint.get('issue_types'),
            issue_status=sprint.get('issue_status'),
            issue_categories=sprint.get('issue_categories')
        )
        if _sprint.project.connection.type == 'jira':
            _sprint.queries = {
                'jqls': _generate_jqls(sprint)
            }
    return {
        'title': 'Succeed To Create Project',
        'detail': {
            'sprint_id': _sprint.uuid,
            'jqls': _sprint.queries.get('jqls'),
        }
    }, 200


if __name__ == '__main__':
    print(u'This is a service of JIRA sprint')
