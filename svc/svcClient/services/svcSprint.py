#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pony.orm import db_session, select, get
from models.models import Tracker, Project, Sprint, IssueCaptureSprintLevel, IssueConfig, CaseConfig
import logging


@db_session
def list_sprint():
    """
    List ALl Sprint
    :return:
    """
    sprints = list()
    for item in select(s for s in Sprint if s.status in ['active', 'disable']).order_by(Sprint.name):
        logging.debug('Get sprint %s[%s] info' % (item.uuid, item.name))
        sprints.append({
            'id': item.uuid,
            'name': item.name,
            'project_name': item.project.name,
            'issue_config_sprint_value': item.issue_config.sprint.get('value'),
            'case_config_sprint_value': item.case_config.sprint.get('value'),
            'status': item.status
        })
    return {
        'count': len(sprints),
        'results': sprints
    }


@db_session
def get_sprint(sprint_id: str):
    """
    Get Sprint
    :param sprint_id:
    :return:
    """
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    capture_time_list = list()
    for capture in select(i for i in IssueCaptureSprintLevel
                          if str(i.sprint.uuid) == sprint_id).order_by(IssueCaptureSprintLevel.capture_time):
        capture_time_list.append(capture.capture_time)
    return {
        'id': sprint.uuid,
        'name': sprint.name,
        'project_id': sprint.project.uuid,
        'project_name': sprint.project.name,
        'issue_config': {
            'sprint': sprint.issue_config.sprint,
            'requirement': sprint.issue_config.requirement,
            'version': sprint.issue_config.version,
            'rc': sprint.issue_config.rc,
            'type': sprint.issue_config.type,
            'since': sprint.issue_config.since,
            'category': sprint.issue_config.category,
            'status': sprint.issue_config.sprint,
        },
        'case_config': {},
        'status': sprint.status,
        'start_time': int(capture_time_list[0].timestamp()) if len(capture_time_list) > 0 else '',
        'end_time': int(capture_time_list[-1].timestamp()) if len(capture_time_list) > 0 else '',
    }


@db_session
def set_sprint_status(sprint_id: str, body: dict):
    """
    Change Sprint Status: active/disable
    :param sprint_id:
    :param body: {
        'status': 'active',
    }
    :return:
    """
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    sprint.status = body.get('status').lower()
    return {
        'id': sprint.uuid,
        'status': sprint.status,
    }


@db_session
def add_sprint(body: dict):
    """
    Add Sprint
    :param body: {
        'name': string,
        'project_id': string,
        'issue_config': {
            'sprint': {
                'field': 'string',
                'value': ['string'],
            },
            'requirement': {
                'field': 'string',
                'value': ['string'],
            },
            'version': {
                'field': 'string',
                'value': ['string'],
            },
            'rc': {
                'field': 'string',
                'value': ['string'],
            },
            'type': {
                'field': 'string',
                'value': ['string'],
            },
            'since': {
                'field': 'string',
                'newfeature': ['string'],
                'improve': ['string'],
                'qamissed': ['string'],
                'customer': ['string'],
            },
            'category': {
                'field': 'string',
                'newfeature': ['string'],
                'regression': ['string'],
                'previous': ['string'],
            },
            'status': {
                'field': 'string',
                'fixing': ['string'],
                'fixed': ['string'],
                'verified': ['string'],
            },
        },
        'case_config': {},
    }
    :return:
    """
    logging.debug('Get Project %s' % body.get('project_id'))
    project = get(p for p in Project if str(p.uuid) == body.get('project_id'))
    if project:
        logging.debug('Got it')
    else:
        logging.debug('No this project')
    logging.debug('Generate PROJECT[%s] Issue Config' % project.name)
    issue_config = IssueConfig(
        sprint=body['issue_config'].get('sprint'),
        requirement=body['issue_config'].get('requirement'),
        version=body['issue_config'].get('version'),
        rc=body['issue_config'].get('rc'),
        type=body['issue_config'].get('type'),
        since=body['issue_config'].get('since'),
        category=body['issue_config'].get('category'),
        status=body['issue_config'].get('status')
    )
    logging.debug('Generate PROJECT[%s] Case Config' % project.name)
    case_config = CaseConfig()
    logging.debug('Add New Sprint %s' % body.get('name'))
    sprint = Sprint(
        name=body.get('name'),
        project=project,
        issue_config=issue_config,
        case_config=case_config
    )
    logging.debug('Complete to add sprint[%s]' % sprint.uuid)
    # logging.debug('Get issue tracker %s' % _project.tracker.get('issue').get('id'))
    # _issue_tracker = get(t for t in Tracker if str(t.uuid) == _project.tracker.get('issue').get('id'))
    # if _issue_tracker.type == 'jira':
    #     logging.debug('Issue tracker is JIRA')
    #     _sprint.queries = {
    #         'issue': {
    #             'jira': generateQueries.generate_jqls(_project.project['issue']['key'], sprint_info)
    #         }
    #     }
    #     logging.debug('Complete to generate issue queries')
    return {
        'id': sprint.uuid,
        'name': sprint.name,
        'project_id': sprint.project.uuid,
        'project_name': sprint.project.name,
        'issue_config': {
            'sprint': sprint.issue_config.sprint,
            'requirement': sprint.issue_config.requirement,
            'version': sprint.issue_config.version,
            'rc': sprint.issue_config.rc,
            'type': sprint.issue_config.type,
            'since': sprint.issue_config.since,
            'category': sprint.issue_config.category,
            'status': sprint.issue_config.sprint,
        },
        'case_config': {},
        'status': sprint.status,
        'start_time': '',
        'end_time': '',
    }


@db_session
def update_sprint(sprint_id: str, body: dict):
    """
    Update Sprint
    :param sprint_id:
    :param body:
    :return:
    """
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    capture_time_list = list()
    for capture in select(i for i in IssueCaptureSprintLevel
                          if str(i.sprint.uuid) == sprint_id).order_by(IssueCaptureSprintLevel.capture_time):
        capture_time_list.append(capture.capture_time)
    project = get(p for p in Project if str(p.uuid) == body.get('project_id'))
    sprint.name = body.get('name')
    sprint.project = project
    sprint.issue_config.sprint = body['issue_config'].get('sprint')
    sprint.issue_config.requirement = body['issue_config'].get('requirement')
    sprint.issue_config.version = body['issue_config'].get('version')
    sprint.issue_config.rc = body['issue_config'].get('rc')
    sprint.issue_config.type = body['issue_config'].get('type')
    sprint.issue_config.since = body['issue_config'].get('since')
    sprint.issue_config.category = body['issue_config'].get('category')
    sprint.issue_config.status = body['issue_config'].get('status')
    # sprint.case_config = body['case_config']
    return {
        'id': sprint.uuid,
        'name': sprint.name,
        'project_id': sprint.project.uuid,
        'project_name': sprint.project.name,
        'issue_config': {
            'sprint': sprint.issue_config.sprint,
            'requirement': sprint.issue_config.requirement,
            'version': sprint.issue_config.version,
            'rc': sprint.issue_config.rc,
            'type': sprint.issue_config.type,
            'since': sprint.issue_config.since,
            'category': sprint.issue_config.category,
            'status': sprint.issue_config.status,
        },
        'case_config': {},
        'status': sprint.status,
        'start_time': int(capture_time_list[0].timestamp()) if len(capture_time_list) > 0 else '',
        'end_time': int(capture_time_list[-1].timestamp()) if len(capture_time_list) > 0 else '',
    }


if __name__ == '__main__':
    print(u'This is SERVICE of sprint')
