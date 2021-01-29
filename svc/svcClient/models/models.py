#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from db.db import db
from pony.orm import Required, PrimaryKey, Set, Json, Optional
import uuid
from datetime import datetime


class Tracker(db.Entity):
    """
    Tracker Information
    """
    _table_ = 'tracker'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    name = Required(str)

    # Type: jira
    type = Required(str)

    # jira: {'host': 'string', 'account': 'string'}
    info = Required(Json, default={'host': '', 'account': ''})

    # jira: password
    token = Required(str)

    # Status: active, disable, delete
    status = Required(str, default='active')

    issue_projects = Set('Project', reverse='issue_tracker')
    case_projects = Set('Project', reverse='case_tracker')


class Project(db.Entity):
    """
    Project Information
    """
    _table_ = 'project'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    name = Required(str)

    # Issue Tracker
    issue_tracker = Optional(Tracker)

    # Issue Project Info: {'project_key': 'string', 'project_value': 'string'}
    issue_project = Required(Json, default={'project_key': '', 'project_value': ''})

    # Case Tracker
    case_tracker = Optional(Tracker)

    # Case Project Info: {'project_key': 'string', 'project_value': 'string'}
    case_project = Required(Json, default={'project_key': '', 'project_value': ''})

    # Status: active, disable, delete
    status = Required(str, default='active')

    sprints = Set('Sprint')
    issue_capture_static_overview = Set('IssueCaptureStaticOverview')


class IssueConfig(db.Entity):
    """
    Sprint Issue Configuration
    """
    _table_ = 'issue_config'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)

    # Issue Found in Sprint
    sprint = Required(Json, default={'field': '', 'value': []})

    # Issue Found in Requirement
    requirement = Required(Json, default={'field': '', 'value': []})

    # Issue Found in Version
    version = Required(Json, default={'field': '', 'value': []})

    # Issue Found in RC
    rc = Required(Json, default={'field': '', 'value': []})

    # Issue Type
    type = Required(Json, default={'field': '', 'value': []})

    # Issue Found Since
    since = Required(Json, default={'field': '', 'newfeature': [], 'improve': [], 'customer': [], 'qamissed': []})

    # Issue Category
    category = Required(Json, default={'field': '', 'newfeature': [], 'regression': [], 'previous': []})

    # Issue Status
    status = Required(Json, default={'field': '', 'fixing': [], 'fixed': [], 'verified': []})

    sprints = Set('Sprint')


class CaseConfig(db.Entity):
    """
    Sprint Case Configuration
    """
    _table_ = 'case_config'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)

    # Case Created in Sprint
    sprint = Required(Json, default={'field': '', 'value': []})

    # Case Created in Requirement
    requirement = Required(Json, default={'field': '', 'value': []})

    # Case Created in Version
    version = Required(Json, default={'field': '', 'value': []})

    sprints = Set('Sprint')


class Sprint(db.Entity):
    """
    Sprint Information
    """
    _table_ = 'sprint'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    name = Required(str)
    project = Required(Project)
    issue_config = Required(IssueConfig)
    case_config = Required(CaseConfig)

    # Status: active, disable, delete
    status = Required(str, default='active')

    issue_capture_sprint_level = Set('IssueCaptureSprintLevel')
    issue_capture_req_level = Set('IssueCaptureReqLevel')
    issue_capture_static_project = Set('IssueCaptureStaticProject')
    issue_capture_static_sprint = Set('IssueCaptureStaticSprint')


class IssueCaptureSprintLevel(db.Entity):
    """
    Capture for Sprint Level Issue Data
    """
    _table_ = 'issue_capture_sprint_level'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime, default=datetime.now())
    sprint = Required(Sprint)

    # Issue Status: {'total': int, 'fixing': int, 'fixed': int, 'verified': int}
    status = Required(Json)

    # Issue Category: {'newfeature': int, 'regression': int, 'previous': int, 'others': int}
    category = Required(Json)

    # Issue Found Since: {'newfeature': int, 'improve': int, 'qamissed': int, 'customer': int, 'others': int}
    since = Required(Json)

    # Issue Found in RC: {'rc1': int, 'rc2': int, 'rc3': int, ...}
    rc = Required(Json)


class IssueCaptureReqLevel(db.Entity):
    """
    Capture for Sprint Requirement Level Issue Data
    """
    _table_ = 'issue_capture_req_level'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime, default=datetime.now())
    sprint = Required(Sprint)

    # Requirement Name
    name = Required(str)

    # Issue Status: {'total': int, 'fixing': int, 'fixed': int, 'verified': int}
    status = Required(Json, default={"total": 0, "fixing": 0, "fixed": 0, "verified": 0})

    # Issue Found in RC: {'rc1': int, 'rc2': int, 'rc3': int, ...}
    rc = Required(Json, default={})


class IssueCaptureStaticOverview(db.Entity):
    """
    Capture Static Data for Overview
    """
    _table_ = 'issue_capture_static_overview'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime, default=datetime.now())
    project = Required(Project)
    in_release = Required(Json, default={"total": 0})
    from_customer = Required(Json, default={"total": 0})


class IssueCaptureStaticProject(db.Entity):
    """
    Capture Static Data for Project
    """
    _table_ = 'issue_capture_static_project'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime, default=datetime.now())
    sprint = Required(Sprint)
    in_release = Required(Json, default={"total": 0})
    from_customer = Required(Json, default={"total": 0})


class IssueCaptureStaticSprint(db.Entity):
    """
    Capture Static Data for Sprint
    """
    _table_ = 'issue_capture_static_sprint'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime, default=datetime.now())
    sprint = Required(Sprint)
    in_rc = Required(Json, default={})
    found_since = Required(Json, default={"newfeature": 0, "improve": 0, "qamissed": 0, "others": 0})
    in_req = Required(Json, default={})
