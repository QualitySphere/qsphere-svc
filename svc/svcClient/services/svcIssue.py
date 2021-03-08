#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pony.orm import db_session, select, get
from models.models import *
from utils.jiraClient import JiraSession
from threading import Thread
from datetime import datetime
import logging
import numpy


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
        '%s = %s' % (sprint.issue_config.sprint['field'], sprint.issue_config.sprint['value'][0]),
        __jql_condition(sprint.issue_config.type['field'], sprint.issue_config.type['value']),
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
    summary_dict[dict_key] = int(jira_rsp['total'])
    logging.info('Succeed to get %s issue count: %s' % (dict_key, summary_dict[dict_key]))
    return True


def __get_issue_count_from_jira(jira_info, jqls):
    """
    Search JIRA Issues and return count summary
    :param jira_info: JIRA info
    :param jqls: JIRA JQLs
    :return:
    """
    issue_summary = dict()
    # logging.info('Access JIRA and JQL search issue data via multi-thread')
    # threads = list()
    # for key, jql in jqls.items():
    #     threads.append(
    #         Thread(
    #             name='SearchJiraThread-%s' % key,
    #             target=__get_issue_count_from_jira_thread,
    #             args=(jira_info, jql, issue_summary, key)
    #         )
    #     )
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # for t in threads:
    #     t.join()
    # logging.info('Check all threads results')
    # for key, jql in jqls.items():
    #     assert issue_summary.get(key) is not None, 'Failed to get value of %s' % key
    # logging.info('Jira issue data collection complete')
    # return issue_summary
    logging.info('Access JIRA and JQL search issue data')
    with JiraSession(jira_info['host'], jira_info['account'], jira_info['password']) as jira_session:
        for key, jql in jqls.items():
            # logging.info('Get issue count via JQL[%s]' % jql)
            jira_rsp = jira_session.search_issues(jql)
            issue_summary[key] = int(jira_rsp['total'])
            logging.info('Succeed to get %s issue count: %s' % (key, issue_summary[key]))
    for key, jql in jqls.items():
        assert issue_summary.get(key) is not None, 'Failed to get value of %s' % key
    logging.info('Jira issue data collection complete')
    return issue_summary


def __format_issue_data(source_data: dict, source_rc: list, source_req: list):
    """
    Format issue source data
    :param source_data:
    :param source_rc:
    :param source_req:
    :return:
    """
    logging.info('Init formatted issue data')
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

    formatted_data['sprint']['status']['total'] = numpy.sum(list(formatted_data['sprint']['status'].values()))
    logging.info('Calculate sprint.status.total: %s' % formatted_data['sprint']['status']['total'])

    formatted_data['sprint']['category']['others'] = numpy.subtract(
        formatted_data['sprint']['status']['total'],
        numpy.sum(list(formatted_data['sprint']['category'].values()))
    )
    logging.info('Calculate sprint.category.others: %s' % formatted_data['sprint']['category']['others'])

    logging.info('Calculate for sprint.since.others')
    formatted_data['sprint']['since']['others'] = numpy.subtract(
        formatted_data['sprint']['status']['total'],
        numpy.sum([
            formatted_data['sprint']['since']['newfeature'],
            formatted_data['sprint']['since']['improve'],
            formatted_data['sprint']['since']['qamissed']
        ])
    )

    for __rc in source_rc:
        logging.info('Calculate for sprint.rc.%s' % __rc)
        formatted_data['sprint']['rc'][__rc] = source_data['sprint.rc.%s' % __rc]

    for __req in source_req:
        logging.info('Calculate for req.%s.status' % __req)
        formatted_data['requirement'][__req] = {
            'status': {
                'fixing': source_data['req.%s.status.fixing' % __req],
                'fixed': source_data['req.%s.status.fixed' % __req],
                'verified': source_data['req.%s.status.verified' % __req],
            },
            'rc': dict(),
        }
        for __rc in source_rc:
            logging.info('Calculate for req.%s.rc.%s' % (__req, __rc))
            formatted_data['requirement'][__req]['rc'][__rc] = source_data['req.%s.rc.%s' % (__req, __rc)]

    logging.info('Update static sprint.in_req')
    formatted_data['static']['sprint.in_req'] = dict()
    for __req in source_req:
        formatted_data['static']['sprint.in_req'][__req] = numpy.sum(
            list(formatted_data['requirement'][__req]['status'].values())
        )

    logging.info('Update static sprint.found_since')
    formatted_data['static']['sprint.found_since'] = formatted_data['sprint']['since']

    logging.info('Update static sprint.in_rc')
    formatted_data['static']['sprint.in_rc'] = formatted_data['sprint']['rc']

    logging.info('Update static sprint.in_release')
    formatted_data['static']['project.in_release'] = {
        'total': formatted_data['sprint']['status']['total'],
    }

    logging.info('Update static project.from_customer')
    formatted_data['static']['project.from_customer'] = {
        'total': formatted_data['sprint']['since']['customer'],
    }
    logging.info('Complete to format issue data')
    return formatted_data


@db_session
def __collect_active_sprint_issue_data_from_jira(sprint_id: str):
    """
    Collect active sprint's issue data from JIRA Sprint
    :param sprint_id:
    :return:
    """
    logging.info('Start to collect ACTIVE sprint %s issue data' % sprint_id)
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

    logging.info('Insert capture data into DB')
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

    static_sprint = get(s for s in IssueCaptureStaticSprint if str(s.sprint.uuid) == str(sprint.uuid))
    if static_sprint:
        logging.info('Update sprint %s static data into DB' % sprint.uuid)
        static_sprint.capture_time = capture_time
        static_sprint.in_rc = issue_data['static']['sprint.in_rc']
        static_sprint.found_since = issue_data['static']['sprint.found_since']
        static_sprint.in_req = issue_data['static']['sprint.in_req']
    else:
        logging.info('Add sprint %s static data into DB' % sprint.uuid)
        IssueCaptureStaticSprint(
            capture_time=capture_time,
            sprint=sprint,
            in_rc=issue_data['static']['sprint.in_rc'],
            found_since=issue_data['static']['sprint.found_since'],
            in_req=issue_data['static']['sprint.in_req']
        )

    static_project = get(p for p in IssueCaptureStaticProject if str(p.sprint.uuid) == str(sprint.uuid))
    if static_project:
        logging.info('Update project %s static data into DB' % project.uuid)
        static_project.capture_time = capture_time
        static_project.in_release = issue_data['static']['project.in_release']
        static_project.from_customer = issue_data['static']['project.from_customer']
    else:
        logging.info('Add project %s static data into DB' % project.uuid)
        IssueCaptureStaticProject(
            capture_time=capture_time,
            sprint=sprint,
            in_release=issue_data['static']['project.in_release'],
            from_customer=issue_data['static']['project.from_customer']
        )

    static_overview = get(o for o in IssueCaptureStaticOverview if str(o.project.uuid) == str(project.uuid))
    if static_overview:
        logging.info('Update overview static data into DB')
        static_overview.capture_time = capture_time
        items = select(s for s in IssueCaptureStaticProject
                       if str(s.sprint.project.uuid) == str(project.uuid))
        in_release_total = list()
        from_customer_total = list()
        for item in items:
            in_release_total.append(int(item.in_release['total']))
            from_customer_total.append(int(item.from_customer['total']))
        static_overview.in_release = {
            'total': numpy.sum(in_release_total)
        }
        static_overview.from_customer = {
            'total': numpy.sum(from_customer_total)
        }
    else:
        logging.info('Add overview static data into DB')
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
    logging.info('Start to collect DISABLE sprint %s issue data' % sprint_id)
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

    static_project = get(p for p in IssueCaptureStaticProject if str(p.sprint.uuid) == str(sprint.uuid))
    if static_project:
        logging.info('Update project %s static data into DB' % project.uuid)
        static_project.capture_time = capture_time
        static_project.from_customer = {
            'total': int(customer_total)
        }

    static_overview = get(o for o in IssueCaptureStaticOverview if str(o.project.uuid) == str(project.uuid))
    items = select(s for s in IssueCaptureStaticProject if str(s.sprint.project.uuid) == str(project.uuid))
    from_customer_total = list()
    for item in items:
        from_customer_total.append(int(item.from_customer['total']))
    if static_overview:
        logging.info('Update overview static data into DB')
        static_overview.capture_time = capture_time
        static_overview.from_customer = {
            'total': numpy.sum(from_customer_total)
        }

    return True


@db_session
def __sync_sprint_issue_data(sprint_id: str, sync_result: dict):
    """
    Start to sync Sprint issue data
    :param sprint_id:
    :param sync_result:
    :return:
    """
    sync_result[sprint_id] = False
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    tracker = get(t for t in Tracker if t.uuid == sprint.project.issue_tracker.uuid)
    if tracker.type == 'jira':
        with JiraSession(
                server=tracker.info['host'],
                account=tracker.info['account'],
                password=tracker.token
        ) as j_session:
            assert j_session.get_user() == tracker.info['account']
        if sprint.status == 'active':
            __collect_active_sprint_issue_data_from_jira(sprint_id)
        elif sprint.status == 'disable':
            __collect_disable_sprint_issue_data_from_jira(sprint_id)
    sync_result[sprint_id] = True
    return sync_result[sprint_id]


@db_session
def sync_issue_data(sprint_id=None):
    """
    Start to sync Sprint(s) issue data
    :param sprint_id:
    :return:
    """
    if sprint_id:
        logging.info('Search sprint %s from DB' % sprint_id)
        sprints = [
            get(s for s in Sprint
                if str(s.uuid) == sprint_id
                and s.status != 'delete'
                and s.project.status == 'active'
                and s.project.issue_tracker.status == 'active')
        ]
    else:
        logging.info('Search all sprints from DB')
        sprints = select(s for s in Sprint
                         if s.status != 'delete'
                         and s.project.status == 'active'
                         and s.project.issue_tracker.status == 'active')
    if not sprints:
        logging.info('No sprints need to be sync')
        return True
    # 多线程并行同步 sprint 数据
    threads = list()
    threads_result = dict()
    for sprint in sprints:
        logging.info('Start to sync data for sprint %s:%s' % (sprint.uuid, sprint.name))
        threads.append(
            Thread(
                name='SyncIssueDataThread-%s' % str(sprint.uuid),
                target=__sync_sprint_issue_data,
                args=(str(sprint.uuid), threads_result)
            )
        )
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    # # 单线程同步 Sprint 数据
    # for sprint in sprints:
    #     logging.info('Start to sync data for sprint %s' % sprint.name)
    #     __sync_sprint_issue_data(str(sprint.uuid))
    logging.info('Check all sync task results')
    assert False not in threads_result.values(), 'Failed to complete sync data for sprint: %s' % threads_result
    # for sprint in sprints:
    #     assert sprint.sync_status == 'pass', 'Failed to complete sync data for sprint: %s' % str(sprint.uuid)
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
