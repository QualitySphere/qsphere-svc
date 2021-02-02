#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pony.orm import db_session, select, get, sum
from models.models import *
from utils.jiraClient import JiraSession
from threading import Thread
from datetime import datetime
import logging


def __jql_condition(field_name: str, field_value_list: list):
    """
    Generate JQL Condition
    :param field_name:
    :param field_value_list:
    :return: 'filed IN (value_1, value_2)'
    """
    return '%s IN (%s)' % (field_name, str(field_value_list).strip('[|]'))


def __generate_jql(sprint):
    """
    Generate JQLs for sprint
    :param sprint: object in DB
    :return:
    """
    logging.info('Start to generate JQL for %s' % sprint.uuid)
    customer_jql_base = ' AND '.join([
        'project = %s' % sprint.project.issue_project['project_key'],
        __jql_condition(sprint.issue_config.type['field'], sprint.issue_config.type['value']),
        __jql_condition(sprint.issue_config.version['field'], sprint.issue_config.version['value']),
        __jql_condition(sprint.issue_config.since['field'], sprint.issue_config.since['customer'])
        ])
    sprint_jql_base = ' AND '.join([
        'project = %s' % sprint.project.issue_project['project_key'],
        __jql_condition(sprint.issue_config.type['field'], sprint.issue_config.type['value']),
        __jql_condition(sprint.issue_config.sprint['field'], sprint.issue_config.sprint['value']),
        __jql_condition(sprint.issue_config.version['field'], sprint.issue_config.version['value'])
    ])
    jqls = {
        'sprint.status.fixing': ' AND '.join([
            sprint_jql_base,
            __jql_condition(sprint.issue_config.status['field'], sprint.issue_config.status['fixing'])
        ]),
        'sprint.status.fixed': ' AND '.join([
            sprint_jql_base,
            __jql_condition(sprint.issue_config.status['field'], sprint.issue_config.status['fixed'])
        ]),
        'sprint.status.verified': ' AND '.join([
            sprint_jql_base,
            __jql_condition(sprint.issue_config.status['field'], sprint.issue_config.status['verified'])
        ]),
        'sprint.category.newfeature': ' AND '.join([
            sprint_jql_base,
            __jql_condition(sprint.issue_config.category['field'], sprint.issue_config.category['newfeature'])
        ]),
        'sprint.category.regression': ' AND '.join([
            sprint_jql_base,
            __jql_condition(sprint.issue_config.category['field'], sprint.issue_config.category['regression'])
        ]),
        'sprint.category.previous': ' AND '.join([
            sprint_jql_base,
            __jql_condition(sprint.issue_config.category['field'], sprint.issue_config.category['previous'])
        ]),
        'sprint.since.newfeature': ' AND '.join([
            sprint_jql_base,
            __jql_condition(sprint.issue_config.since['field'], sprint.issue_config.since['newfeature'])
        ]),
        'sprint.since.improve': ' AND '.join([
            sprint_jql_base,
            __jql_condition(sprint.issue_config.since['field'], sprint.issue_config.since['improve'])
        ]),
        'sprint.since.qamissed': ' AND '.join([
            sprint_jql_base,
            __jql_condition(sprint.issue_config.since['field'], sprint.issue_config.since['qamissed'])
        ]),
        'project.since.customer': customer_jql_base,  # Customer issue should be tracked out of Sprint
    }
    for rc in sprint.issue_config.rc['value']:
        jqls['sprint.rc.%s' % rc] = ' AND '.join([
            sprint_jql_base,
            '%s IN ("%s")' % (sprint.issue_config.rc['field'], rc)
        ])
    for req in sprint.issue_config.requirement['value']:
        jqls['req.%s.status.fixing' % req] = ' AND '.join([
            sprint_jql_base,
            '%s in ("%s")' % (sprint.issue_config.requirement['field'], req),
            __jql_condition(sprint.issue_config.status['field'], sprint.issue_config.status['fixing'])
        ])
        jqls['req.%s.status.fixed' % req] = ' AND '.join([
            sprint_jql_base,
            '%s in ("%s")' % (sprint.issue_config.requirement['field'], req),
            __jql_condition(sprint.issue_config.status['field'], sprint.issue_config.status['fixed'])
        ])
        jqls['req.%s.status.verified' % req] = ' AND '.join([
            sprint_jql_base,
            '%s in ("%s")' % (sprint.issue_config.requirement['field'], req),
            __jql_condition(sprint.issue_config.status['field'], sprint.issue_config.status['verified'])
        ])
        for rc in sprint.issue_config.rc['value']:
            jqls['req.%s.rc.%s' % (req, rc)] = ' AND '.join([
                jqls['sprint.rc.%s' % rc],
                '%s in ("%s")' % (sprint.issue_config.requirement['field'], req)
            ])
    logging.info('JQLs: %s' % jqls)
    return jqls


def __get_issue_count_from_jira_thread(jira_info, jql, summary_dict, dict_key):
    """
    Single thread to get issue count from jira
    :param jira_info:
    :param jql:
    :param summary_dict:
    :param dict_key:
    :return:
    """
    logging.info('Get issue count via JQL[%s]' % jql)
    with JiraSession(jira_info['host'], jira_info['account'], jira_info['password']) as jira_session:
        jira_rsp = jira_session.search_issues(jql)
    if jira_rsp.get('total') is None:
        raise Exception(str(jira_rsp))
    summary_dict[dict_key] = int(jira_rsp['total'])
    logging.debug('Succeed to get %s issue count: %s' % (dict_key, summary_dict[dict_key]))
    return True


def __get_issue_count_from_jira(jira_info, jqls):
    """
    Search JIRA Issues and return count summary
    :param jira_info: JIRA info
    :param jqls: JIRA JQLs
    :return:
    """
    issue_summary = dict()
    logging.info(u'多线程登录 JIRA 用 JQL 收集所有数据')
    threads = list()
    for key, jql in jqls.items():
        threads.append(
            Thread(
                target=__get_issue_count_from_jira_thread,
                args=(jira_info, jql, issue_summary, key)
            )
        )
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    return issue_summary


def __format_issue_data(source_data: dict, source_rc: list, source_req: list):
    """
    Format issue source data
    :param source_data:
    :param source_rc:
    :param source_req:
    :return:
    """
    logging.info('Init formatted data')
    formatted_data = {
        'sprint': {
            'status': {
                'fixing': source_data['sprint.status.fixing'],
                'fixed': source_data['sprint.status.fixed'],
                'verified': source_data['sprint.status.verified'],
            },
            'category': {
                'newfeature': source_data['sprint.category.newfeature'],
                'regression': source_data['sprint.category.regression'],
                'previous': source_data['sprint.category.previous'],
            },
            'since': {
                'newfeature': source_data['sprint.since.newfeature'],
                'improve': source_data['sprint.since.improve'],
                'qamissed': source_data['sprint.since.qamissed'],
                'customer': source_data['project.since.customer'],
            },
            'rc': dict(),
        },
        'requirement': dict(),
        'static': dict(),
    }

    logging.info('Calculate sprint.status.total')
    formatted_data['sprint']['status']['total'] = sum(formatted_data['sprint']['status'].values())

    # Calculate sprint.category.others
    formatted_data['sprint']['category']['others'] = \
        formatted_data['sprint']['status']['total'] - sum(formatted_data['sprint']['category'].values())

    # Calculate sprint.since.others
    formatted_data['sprint']['since']['others'] = \
        formatted_data['sprint']['status']['total'] - \
        formatted_data['sprint']['since']['newfeature'] - \
        formatted_data['sprint']['since']['improve'] - \
        formatted_data['sprint']['since']['qamissed']

    # Calculate sprint.rc
    for __rc in source_rc:
        formatted_data['sprint']['rc'][__rc] = source_data['sprint.rc.%s' % __rc]

    # Calculate req.$req.status and req.$req.rc
    for __req in source_req:
        formatted_data['requirement'][__req] = {
            'status': {
                'fixing': source_data['req.%s.status.fixing' % __req],
                'fixed': source_data['req.%s.status.fixed' % __req],
                'verified': source_data['req.%s.status.verified' % __req],
            },
            'rc': dict(),
        }
        for __rc in source_rc:
            formatted_data['requirement'][__req]['rc'][__rc] = source_data['req.%s.rc.%s' % (__req, __rc)]

    # Update static sprint.found_since
    formatted_data['static']['sprint.in_req'] = dict()
    for __req in source_req:
        formatted_data['static']['sprint.in_req'][__req] = sum(formatted_data['requirement'][__req]['status'].values())

    # Update static sprint.found_since
    formatted_data['static']['sprint.found_since'] = formatted_data['sprint']['since']

    # Update static sprint.in_rc
    formatted_data['static']['sprint.in_rc'] = formatted_data['sprint']['rc']

    # Update static project.in_release
    formatted_data['static']['project.in_release'] = {
        'total': formatted_data['sprint']['status']['total'],
    }

    logging.info('Update static project.from_customer')
    formatted_data['static']['project.from_customer'] = {
        'total': formatted_data['sprint']['since']['customer'],
    }
    return formatted_data


@db_session
def __collect_active_sprint_issue_data_from_jira(sprint_id: str):
    """
    Collect active sprint's issue data from JIRA Sprint
    :param sprint_id:
    :return:
    """
    logging.info('Start to collect ACTIVE sprint issue data: %s' % sprint_id)
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    project = get(p for p in Project if str(p.uuid) == str(sprint.project.uuid))
    capture_time = datetime.now()
    jqls = __generate_jql(sprint)
    jira_info = {
        'host': project.issue_tracker.info['host'],
        'account': project.issue_tracker.info['account'],
        'password': project.issue_tracker.token,
    }
    issue_data = __format_issue_data(
        source_data=__get_issue_count_from_jira(jira_info, jqls),
        source_rc=sprint.issue_config.rc['value'],
        source_req=sprint.issue_config.requirement['value']
    )

    # Insert capture data into DB
    IssueCaptureSprintLevel(
        capture_time=capture_time,
        sprint=sprint,
        status=issue_data['sprint']['status'],
        category=issue_data['sprint']['category'],
        since=issue_data['sprint']['since'],
        rc=issue_data['sprint']['rc']
    )
    for __req in sprint.issue_config.requirement['value']:
        IssueCaptureReqLevel(
            capture_time=capture_time,
            sprint=sprint,
            name=__req,
            status=issue_data['requirement'][__req]['status'],
            rc=issue_data['requirement'][__req]['rc']
        )

    # Add/Update sprint static data into DB
    static_sprint = get(s for s in IssueCaptureStaticSprint if str(s.sprint.uuid) == str(sprint.uuid))
    if static_sprint:
        static_sprint.capture_time = capture_time
        static_sprint.in_rc = issue_data['static']['sprint.in_rc']
        static_sprint.found_since = issue_data['static']['sprint.found_since']
        static_sprint.in_req = issue_data['static']['sprint.in_req']
    else:
        IssueCaptureStaticSprint(
            capture_time=capture_time,
            sprint=sprint,
            in_rc=issue_data['static']['sprint.in_rc'],
            found_since=issue_data['static']['sprint.found_since'],
            in_req=issue_data['static']['sprint.in_req']
        )

    # Add/Update project static data into DB
    static_project = get(p for p in IssueCaptureStaticProject if str(p.sprint.uuid) == str(sprint.uuid))
    if static_project:
        static_project.capture_time = capture_time
        static_project.in_release = issue_data['static']['project.in_release']
        static_project.from_customer = issue_data['static']['project.from_customer']
    else:
        IssueCaptureStaticProject(
            capture_time=capture_time,
            sprint=sprint,
            in_release=issue_data['static']['project.in_release'],
            from_customer=issue_data['static']['project.from_customer']
        )

    # Add/Update overview static data into DB
    static_overview = get(o for o in IssueCaptureStaticOverview if str(o.project.uuid) == str(project.uuid))
    if static_overview:
        static_overview.capture_time = capture_time
        static_overview.in_release = {
            'total': sum(s.in_release for s in IssueCaptureStaticProject if str(s.project.uuid) == str(project.uuid))
        }
        static_overview.from_customer = {
            'total': sum(s.from_customer for s in IssueCaptureStaticProject if str(s.project.uuid) == str(project.uuid))
        }
    else:
        IssueCaptureStaticOverview(
            capture_time=capture_time,
            project=project,
            in_release=issue_data['static']['project.in_release'],
            from_customer=issue_data['static']['project.from_customer']
        )

    return True


@db_session
def __collect_disable_sprint_issue_data_from_jira(sprint_id: str):
    """
    Collect disabled sprint issue data from JIRA Sprint
    :param sprint_id:
    :return:
    """
    logging.info('Start to collect DISABLE sprint issue data: %s' % sprint_id)
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    project = get(p for p in Project if str(p.uuid) == str(sprint.project.uuid))
    capture_time = datetime.now()
    customer_jql_base = ' AND '.join([
        'project = %s' % sprint.project.issue_project['project_key'],
        '%s IN (%s)' % (sprint.issue_config.type['field'], str(sprint.issue_config.type['value']).strip('[|]')),
        '%s IN (%s)' % (sprint.issue_config.version['field'], str(sprint.issue_config.version['value']).strip('[|]')),
        '%s IN (%s)' % (sprint.issue_config.since['field'], str(sprint.issue_config.since['customer']).strip('[|]')),
        ])
    with JiraSession(
        project.issue_tracker.info['host'],
        project.issue_tracker.info['account'],
        project.issue_tracker.token
    ) as jira_session:
        customer_total = jira_session.search_issues(customer_jql_base)['total']

    # Add/Update project static data into DB
    static_project = get(p for p in IssueCaptureStaticProject if str(p.sprint.uuid) == str(sprint.uuid))
    if static_project:
        static_project.capture_time = capture_time
        static_project.from_customer = {
            'total': int(customer_total)
        }

    # Add/Update overview static data into DB
    static_overview = get(o for o in IssueCaptureStaticOverview if str(o.project.uuid) == str(project.uuid))
    if static_overview:
        static_overview.capture_time = capture_time
        static_overview.from_customer = {
            'total': sum(s.from_customer for s in IssueCaptureStaticProject if str(s.project.uuid) == str(project.uuid))
        }

    return True


@db_session
def __sync_sprint_issue_data(sprint_id: str):
    """
    Start to sync Sprint issue data
    :param sprint_id:
    :return:
    """
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    if sprint.project.issue_tracker.type == 'jira':
        if sprint.status == 'active':
            __collect_active_sprint_issue_data_from_jira(sprint_id)
        elif sprint.status == 'disable':
            __collect_disable_sprint_issue_data_from_jira(sprint_id)
    return True


@db_session
def sync_issue_data(sprint_id=None):
    """
    Start to sync Sprint(s) issue data
    :param sprint_id:
    :return:
    """
    # Search from DB and sync active/disable sprint(s) data
    if sprint_id:
        sprints = [
            get(s for s in Sprint if s.status != 'delete' and s.project.status == 'active')
        ]
    else:
        sprints = select(s for s in Sprint if s.status != 'delete' and s.project.status == 'active')
    threads = list()
    for sprint in sprints:
        logging.info('Start to sync data for sprint %s' % sprint.name)
        threads.append(
            Thread(
                target=__sync_sprint_issue_data,
                args=(str(sprint.uuid),)
            )
        )
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    logging.info('Complete to sync data for sprints')
    return True


def get_issue_status(sprint_id=None):
    """
    Get Sprint(s) issue verification status
    :param sprint_id:
    :return:
    """
    pass


if __name__ == '__main__':
    print(u'This is SERVICE of issue')
