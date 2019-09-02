#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from clientJira.db.db import db
from pony.orm import Database, Required, PrimaryKey, Set, StrArray, IntArray, Json
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
    status = Required(str, default='active')
    sprints = Set('Sprint')


class Sprint(db.Entity):
    _table_ = 'sprint'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    project = Required(Project)
    name = Required(str)
    version = Required(str)
    features = Required(StrArray)
    rcs = Required(IntArray)
    issue_types = Required(StrArray)
    issue_categories = Required(StrArray)
    status = Required(str, default='active')
    issue_overall = Set('IssueProject')
    issue_sprint = Set('IssueSprint')
    issue_feature = Set('IssueFeature')


class IssueProject(db.Entity):
    _table_ = 'issue_overall'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    total = Required(int)
    categories = Required(Json)
    # category_regression = Required(int)
    # category_previous = Required(int)
    # category_code_change = Required(int)
    # category_others = Required(int)
    since = Required(Json)
    # since_improve = Required(int)
    # since_qa_missed = Required(int)
    # since_customer = Required(int)


class IssueSprint(db.Entity):
    _table_ = 'issue_sprint'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    status = Required(Json)
    # total = Required(int)
    # fixing = Required(int)
    # fixed = Required(int)
    # verified = Required(int)
    categories = Required(Json)
    # category_regression = Required(int)
    # category_previous = Required(int)
    # category_code_change = Required(int)
    # category_others = Required(int)
    since = Required(Json)
    # since_improve = Required(int)
    # since_qa_missed = Required(int)
    # since_customer = Required(int)
    found_in_rcs = Required(IntArray)


class IssueFeature(db.Entity):
    _table_ = 'issue_feature'

    uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    capture_at = Required(datetime)
    sprint = Required(Sprint)
    name = Required(str)
    status = Required(Json)
    # total = Required(int)
    # fixing = Required(int)
    # fixed = Required(int)
    # verified = Required(int)
    found_in_rcs = Required(IntArray)
