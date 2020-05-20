#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
# name = Required(str)
# project = Required(Project)
# version = Required(str)  # sprint version tag
# requirements = Required(StrArray)  # list(): req1, req2
# rcs = Required(StrArray)  # RC tags list: RC1, RC2
# issue = Optional(Json)  # dict(): keys: types, found_since, statuses, categories
# case = Optional(Json)
# queries = Optional(Json)  # dict(): issue: jql,  ...  case: xx
# status = Required(str, default='active')  # active, disable, delete


from pony.orm import db_session, select, get
from models.models import Tracker, Project, Sprint
import logging
from utils import generateQueries


@db_session
def list_sprint(sprint_status=None):
    """
    List ALl Sprint
    :return:
    """
    sprints = list()
    if sprint_status:
        items = select(s for s in Sprint if s.status in sprint_status).order_by(Sprint.name)
    else:
        items = select(s for s in Sprint).order_by(Sprint.name)
    for item in items:
        logging.info('Get sprint %s[%s] info' % (item.uuid, item.name))
        sprints.append({
            'id': item.uuid,
            'name': item.name,
            'project_id': item.project.uuid,
            'project_name': item.project.name,
            'status': item.status
        })
    return sprints


@db_session
def get_sprint(sprint_id: str):
    """
    Get Sprint
    :param sprint_id:
    :return:
    """
    sprint_info = dict()
    item = get(s for s in Sprint if str(s.uuid) == sprint_id)
    if item:
        sprint_info = {
            'id': item.uuid,
            'name': item.name,
            'project_id': item.project.uuid,
            'project_name': item.project.name,
            "version": item.version,
            "requirements": item.requirements,
            "rcs": item.rcs,
            "issue": item.issue,
            "case": item.case,
            "queries": item.queries,
            'status': item.status
        }
    return sprint_info


@db_session
def set_sprint_status(sprint_id: str, sprint_status: str):
    """
    Change Sprint Status: active/disable
    :param sprint_id:
    :param sprint_status:
    :return:
    """
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    sprint.status = sprint_status
    return sprint.status


@db_session
def add_sprint(sprint_info: dict):
    """
    Add Sprint
    :param sprint_info:
    :return:
    """
    _project = get(p for p in Project if str(p.uuid) == sprint_info.get('project_id'))
    _sprint = Sprint(
        name=sprint_info.get('name'),
        project=_project,
        version=sprint_info.get('version'),
        requirements=sprint_info.get('requirements'),
        rcs=sprint_info.get('rcs'),
        issue=sprint_info.get('issue'),
        case=sprint_info.get('case')
    )
    _issue_tracker = get(t for t in Tracker if str(t.uuid) == _project.tracker.get('issue').get('id'))
    logging.warning(_project.project)
    logging.warning(_project.project['issue'])
    logging.warning(_project.project['issue']['key'])
    if _issue_tracker.type == 'jira':
        _sprint.queries = {
            'issue': {
                'jira': generateQueries.generate_jqls(_project.project['issue']['key'], sprint_info)
            }
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
    _sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    _project = get(p for p in Project if str(p.uuid) == sprint_info.get('project_id'))
    _sprint.project = _project
    _sprint.name = sprint_info.get('name')
    _sprint.version = sprint_info.get('version')
    _sprint.requirements = sprint_info.get('requirements')
    _sprint.rcs = sprint_info.get('rcs')
    _sprint.issue = sprint_info.get('issue')
    _sprint.case = sprint_info.get('case')
    _issue_tracker = get(t for t in Tracker if str(t.uuid) == _project.tracker.get('issue').get('id'))
    if _issue_tracker.type == 'jira':
        _sprint.queries = {
            'issue': {
                'jira': generateQueries.generate_jqls(_project.project['issue']['key'], sprint_info)
            }
        }
    return _sprint.uuid


if __name__ == '__main__':
    print(u'This is a service of sprint')
