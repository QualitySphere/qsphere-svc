#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from clientJira.db.db import db
from pony.orm import Database, Required, PrimaryKey, Set, StrArray, IntArray, Json, Optional
import uuid
from datetime import datetime


class Connection(db.Entity):
    _table_ = 'connection'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    type = Required(str, default='jira')
    server = Required(str)
    account = Required(str)
    password = Required(str)
    projects = Set('Project')


class Project(db.Entity):
    _table_ = 'project'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    connection = Required(Connection)
    name = Required(str)
    active = Required(str, default='enable')
    sprints = Set('Sprint')
    # issue_projects = Set('IssueProject')


class Sprint(db.Entity):
    _table_ = 'sprint'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    project = Required(Project)
    name = Required(str)
    version = Required(str)
    issue_types = Required(StrArray)  # Improvement, 缺陷
    features = Required(StrArray)  # 功能1, 功能2
    rcs = Required(StrArray)  # rc1,rc2,rc3,rc4,rc5
    issue_found_since = Required(StrArray, default=['regression_improve', 'qa_missed', 'customer'])
    issue_status = Required(Json)  # fixing: '待办, 进行中, 新发现', fixed: '开发完成', verified: '已关闭'
    issue_categories = Required(StrArray, default=['regression', 'previous', 'newfeature', 'others'])
    queries = Optional(Json)  # jqls
    active = Required(str, default='enable')
    issue_projects = Set('IssueProject')
    issue_sprints = Set('IssueSprint')
    issue_features = Set('IssueFeature')


class IssueProject(db.Entity):
    _table_ = 'issue_project'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    # project = Required(Project)
    sprint = Required(Sprint)
    categories = Required(Json)
    found_since = Required(Json)


class IssueSprint(db.Entity):
    _table_ = 'issue_sprint'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    status = Required(Json)  # total, fixing, fixed, verified
    categories = Required(Json)  # regression, previous, code_change, others
    found_since = Required(Json)  # regression_improve, qa_missed, customer
    found_in_rcs = Required(Json)  # rc1, rc2, rc3, rc4, rc5


class IssueFeature(db.Entity):
    _table_ = 'issue_feature'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    name = Required(str)
    status = Required(Json)  # total, fixing, fixed, verified
    # found_in_rcs = Required(Json)  # rc1, rc2, rc3, rc4, rc5
