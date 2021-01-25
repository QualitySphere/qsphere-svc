#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from db.db import db
from pony.orm import Database, Required, PrimaryKey, Set, StrArray, IntArray, Json, Optional
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
    info = Optional(Json)
    # jira: password
    token = Optional(str)
    # Status: active, disable, delete
    status = Required(str, default='active')


class Project(db.Entity):
    """
    Project Information
    """
    _table_ = 'project'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    name = Required(str)
    # Issue Tracker: {'tracker_id': 'string', 'project_key': 'string', 'project_value': 'string'}
    issue_tracker = Optional(Json)
    # Case Tracker: {'tracker_id': 'string', 'project_key': 'string', 'project_value': 'string'}
    case_tracker = Optional(Json)
    # Status: active, disable, delete
    status = Required(str, default='active')
    sprints = Set('Sprint')


class IssueConfig(db.Entity):
    """
    Sprint Issue Configuration
    """
    _table_ = 'issue_config'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    # Issue Found in Sprint: {'field': 'string', 'value': ['string']}
    issue_sprint = Required(Json)
    # Issue Found in Requirement: {'field': 'string', 'value': ['string']}
    issue_requirement = Required(Json)
    # Issue Found in Version: {'field': 'string', 'value': ['string']}
    issue_version = Required(Json)
    # Issue Found in RC: {'field': 'string', 'value': ['string']}
    issue_rc = Required(Json)
    # Issue Type: {'field': 'string', 'value': ['string']}
    issue_type = Required(Json)
    # Issue Found Since:
    # {'field': 'string',
    # 'newfeature': ['string'], 'improve': ['string'],
    # 'customer': ['string'], 'qamissed': ['string']}
    issue_since = Required(Json)
    # Issue Category:
    # {'field': 'string',
    # 'newfeature': ['string'], 'regression': ['string'], 'previous': ['string']}
    issue_category = Required(Json)
    # Issue Status:
    # {'field': 'string',
    # 'fixing': ['string'], 'fixed': ['string'], 'verified': ['string']}
    issue_status = Required(Json)
    sprints = Set('Sprint')


class CaseConfig(db.Entity):
    """
    Sprint Case Configuration
    """
    _table_ = 'case_config'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    sprints = Set('Sprint')


class Sprint(db.Entity):
    """
    Sprint Information
    """
    _table_ = 'sprint'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    name = Required(str)
    project = Required(Project)
    issue_config = Optional(IssueConfig)
    case_config = Optional(CaseConfig)
    # Status: active, disable, delete
    status = Required(str, default='active')
    issue_capture_sprint_level = Set('IssueCaptureSprintLevel')
    issue_capture_req_level = Set('IssueCaptureReqLevel')
    issue_capture_latest = Set('IssueCaptureLatest')
    # issue_project_latest = Set('IssueProjectLatest')
    # issue_customer_latest = Set('IssueCustomerLatest')
    # issue_sprint_latest = Set('IssueSprintLatest')
    # issue_req_latest = Set('IssueReqLatest')
    # issue_sprint = Set('IssueSprint')
    # issue_req = Set('IssueReq')


class IssueCaptureSprintLevel(db.Entity):
    """
    Capture for Sprint Level Issue Data
    # _table_ = 'issue_sprint'
    """
    _table_ = 'issue_capture_sprint_level'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime)
    sprint = Required(Sprint)
    # Issue Status: {'total': int, 'fixing': int, 'fixed': int, 'verified': int}
    status = Required(Json)
    # Issue Category: {'newfeature': int, 'regression': int, 'previous': int, 'others': int}
    category = Required(Json)
    # Issue Found Since: {'newfeature': int, 'improve': int, 'qamissed': int}
    since = Required(Json)
    # Issue Found in RC: {'rc1': int, 'rc2': int, 'rc3': int, ...}
    rc = Required(Json)


class IssueCaptureReqLevel(db.Entity):
    """
    Capture for Sprint Requirement Level Issue Data
    # _table_ = 'issue_req'
    """
    _table_ = 'issue_capture_req_level'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime)
    sprint = Required(Sprint)
    # Requirement Name
    name = Required(str)
    # Issue Status: {'total': int, 'fixing': int, 'fixed': int, 'verified': int}
    status = Required(Json)
    # Issue Found in RC: {'rc1': int, 'rc2': int, 'rc3': int, ...}
    rc = Optional(Json)


class IssueCaptureLatest(db.Entity):
    """
    Capture for Latest Issue Data
    """
    _table_ = 'issue_capture_latest'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime)
    sprint = Required(Sprint)
    # Capture for project level: {
    # 'category': {'newfeature': int, 'regression': int, 'previous': int, 'others': int},
    # 'since': {'newfeature': int, 'improve': int, 'customer': int, 'qamissed': int}
    # }
    capture_issue_project = Optional(Json)
    # Capture for customer level: {
    # 'customer': int
    # }
    capture_issue_customer = Optional(Json)
    # Capture for sprint level: {
    # 'rc1': int, 'rc2': int, ...
    # }
    capture_issue_sprint = Optional(Json)
    # Capture for requirement level: {
    # 'req1': {'total': int, 'fixing': int, 'fixed': int, 'verified': int},
    # 'req2': {'total': int, 'fixing': int, 'fixed': int, 'verified': int},
    # }
    capture_issue_req = Optional(Json)

#
# class IssueProjectLatest(db.Entity):
#     """
#     项目维度 最新缺陷数据
#     """
#     _table_ = 'issue_project_latest'
#     uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
#     capture_time = Required(datetime)
#     sprint = Required(Sprint)
#     categories = Required(Json)  # 缺陷类别:
#     found_since = Required(Json)  # 缺陷发现来源: new_feature: '', regression_improve: '', qa_missed: ''
#
#
# class IssueCustomerLatest(db.Entity):
#     # 项目维度 最新客户反馈缺陷数量
#     _table_ = 'issue_customer_latest'
#     uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
#     capture_time = Required(datetime)
#     sprint = Required(Sprint)
#     count = Required(int)  # 客户反馈的缺陷数量, 缺陷发现来源: customer
#
#
# class IssueSprintLatest(db.Entity):
#     # 迭代版本维度 最新缺陷数据
#     _table_ = 'issue_sprint_latest'
#     uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
#     capture_time = Required(datetime)
#     sprint = Required(Sprint)
#     rc = Required(str)  # 迭代版本 RC
#     count = Required(int)  # 缺陷数量
#
#
# class IssueReqLatest(db.Entity):
#     # 迭代版本需求维度 最新缺陷数据
#     _table_ = 'issue_req_latest'
#     uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
#     capture_time = Required(datetime)
#     sprint = Required(Sprint)
#     name = Required(str)  # 需求名称
#     status = Required(Json)  # 缺陷状态: total: '', fixing: '', fixed: '', verified: ''
#
