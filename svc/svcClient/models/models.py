#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from svcClient.db.db import db
from pony.orm import Database, Required, PrimaryKey, Set, StrArray, IntArray, Json, Optional
import uuid
from datetime import datetime


class Connection(db.Entity):
    # 连接缺陷/用例管理工具的地址和帐密信息
    _table_ = 'connection'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    type = Required(str, default='issue')  # issue/case
    server_type = Required(str, default='jira')  # jira/zentao/testlink/bugzilla
    server = Required(str)
    account = Required(str)
    password = Required(str)
    projects = Set('Project')


class Project(db.Entity):
    # 项目名称和激活状态
    _table_ = 'project'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    connection = Required(Connection)
    name = Required(str)
    active = Required(str, default='enable')  # enable, disable, delete
    sprints = Set('Sprint')


class Sprint(db.Entity):
    # 迭代循环的信息
    _table_ = 'sprint'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    project = Required(Project)
    name = Required(str)  # 名称
    version = Required(str)  # 迭代版本
    issue_types = Required(StrArray)  # 问题筛选类型: Improvement, 缺陷
    features = Required(StrArray)  # 功能标签列表: 功能1, 功能2, ...
    rcs = Required(StrArray)  # RC标签列表: rc1,rc2,rc3,rc4,rc5, ...
    issue_found_since = Required(StrArray, default=['regression_improve', 'qa_missed', 'new_feature', 'customer'])  # 问题发现来源标签列表
    issue_status = Required(Json)  # 问题状态: fixing: '', fixed: '', verified: ''
    issue_categories = Required(StrArray, default=['regression', 'previous', 'newfeature', 'others'])  # 问题类别标签列表
    queries = Optional(Json)  # 查询语句集: jql/././.
    active = Required(str, default='enable')  # 该迭代的激活状态: enable, disable, delete
    issue_project_latest = Set('IssueProjectLatest')
    issue_customer_latest = Set('IssueCustomerLatest')
    issue_sprint_latest = Set('IssueSprintLatest')
    issue_feature_latest = Set('IssueFeatureLatest')
    issue_sprint = Set('IssueSprint')
    issue_feature = Set('IssueFeature')


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
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    status = Required(Json)  # 缺陷状态: total, fixing, fixed, verified
    categories = Required(Json)  # 缺陷类别: regression: '', previous: '', new_feature: '', others: ''
    found_since = Required(Json)  # 缺陷发现来源: new_feature: '', regression_improve: '', qa_missed: ''
    found_in_rcs = Required(Json)  # 缺陷发现版本: rc1: '', rc2: '', rc3: '', . . .


class IssueSprintLatest(db.Entity):
    # 迭代版本维度 最新缺陷数据
    _table_ = 'issue_sprint_latest'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    rc = Required(str)  # 迭代版本 RC
    count = Required(int)  # 缺陷数量


class IssueFeature(db.Entity):
    # 迭代版本功能维度 缺陷数据
    _table_ = 'issue_feature'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    name = Required(str)  # 功能名称
    status = Required(Json)  # 缺陷状态: total, fixing, fixed, verified
    # found_in_rcs = Required(Json)  # rc1, rc2, rc3, rc4, rc5


class IssueFeatureLatest(db.Entity):
    # 迭代版本功能维度 最新缺陷数据
    _table_ = 'issue_feature_latest'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    name = Required(str)  # 功能名称
    status = Required(Json)  # 缺陷状态: total: '', fixing: '', fixed: '', verified: ''

