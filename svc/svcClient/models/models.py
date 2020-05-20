#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from db.db import db
from pony.orm import Database, Required, PrimaryKey, Set, StrArray, IntArray, Json, Optional
import uuid
from datetime import datetime


class Tracker(db.Entity):
    # Tracker Information
    _table_ = 'tracker'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    name = Required(str)
    type = Required(str)
    info = Optional(Json)  # JIRA: {host: '', account: ''}
    secret = Optional(str)  # JIRA: 'password'
    status = Required(str, default='active')  # active, disable, delete


class Project(db.Entity):
    # Project Information
    _table_ = 'project'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    name = Required(str)
    tracker = Optional(Json)    # {'issue': {'id': 'UUID'}, 'case': {'id': 'UUID'}}
    project = Optional(Json)    # {'issue': {'key': 'value'}, 'case': {'key': 'value'}}
    status = Required(str, default='active')  # active, disable, delete
    sprints = Set('Sprint')


class Sprint(db.Entity):
    # Sprint Information
    _table_ = 'sprint'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    name = Required(str)
    project = Required(Project)
    version = Required(str)  # sprint version tag
    requirements = Required(StrArray)   # list(): req1, req2
    rcs = Required(StrArray)  # RC tags list: RC1, RC2
    issue = Optional(Json)   # dict(): keys: types, found_since, statuses, categories
    case = Optional(Json)
    queries = Optional(Json)  # dict(): keys: case, issue
    status = Required(str, default='active')  # active, disable, delete
    issue_project_latest = Set('IssueProjectLatest')
    issue_customer_latest = Set('IssueCustomerLatest')
    issue_sprint_latest = Set('IssueSprintLatest')
    issue_feature_latest = Set('IssueReqLatest')
    issue_sprint = Set('IssueSprint')
    issue_feature = Set('IssueReq')


class IssueProjectLatest(db.Entity):
    # 项目维度 最新缺陷数据
    _table_ = 'issue_project_latest'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    categories = Required(Json)  # 缺陷类别:
    found_since = Required(Json)  # 缺陷发现来源: new_feature: '', regression_improve: '', qa_missed: ''


class IssueCustomerLatest(db.Entity):
    # 项目维度 最新客户反馈缺陷数量
    _table_ = 'issue_customer_latest'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    count = Required(int)  # 客户反馈的缺陷数量, 缺陷发现来源: customer


class IssueSprint(db.Entity):
    # 迭代版本维度 缺陷数据
    _table_ = 'issue_sprint'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime)
    sprint = Required(Sprint)
    status = Required(Json)  # 缺陷状态: total, fixing, fixed, verified
    categories = Required(Json)  # 缺陷类别: regression: '', previous: '', new_feature: '', others: ''
    found_since = Required(Json)  # 缺陷发现来源: new_feature: '', regression_improve: '', qa_missed: ''
    found_in_rcs = Required(Json)  # 缺陷发现版本: rc1: '', rc2: '', rc3: '', . . .


class IssueSprintLatest(db.Entity):
    # 迭代版本维度 最新缺陷数据
    _table_ = 'issue_sprint_latest'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime)
    sprint = Required(Sprint)
    rc = Required(str)  # 迭代版本 RC
    count = Required(int)  # 缺陷数量


class IssueReq(db.Entity):
    # 迭代版本需求维度 缺陷数据
    _table_ = 'issue_req'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime)
    sprint = Required(Sprint)
    name = Required(str)  # 需求名称
    status = Required(Json)  # 缺陷状态: total, fixing, fixed, verified
    # found_in_rcs = Required(Json)  # rc1, rc2, rc3, rc4, rc5


class IssueReqLatest(db.Entity):
    # 迭代版本需求维度 最新缺陷数据
    _table_ = 'issue_req_latest'
    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_time = Required(datetime)
    sprint = Required(Sprint)
    name = Required(str)  # 需求名称
    status = Required(Json)  # 缺陷状态: total: '', fixing: '', fixed: '', verified: ''

