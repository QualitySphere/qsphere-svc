#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://qualitysphere.github.io/images/point.png
# https://qualitysphere.gitee.io/images/point.png


from pony.orm import db_session, get, select
from models.models import *
import numpy


def __reload_issue_policy_data(policy_body: dict):
    """
    重新加载缺陷规则的数据
    :param policy_body:
    :return:
    """
    __policy_info = dict()
    for level in ['project', 'sprint']:
        __policy_info[level] = dict()
        for item in policy_body[level].items():
            __policy_info[level][item['key']] = {
                'weight': item['weight'],
                's': item['s'],
                'a': item['a'],
                'b': item['b'],
                'c': item['c'],
                'd': item['d'],
            }
    return __policy_info


@db_session
def add_grade_policy(body: dict):
    item = GradePolicy(
        name=body['name'],
        policy_conf={
            'project': body['project'],
            'sprint': body['sprint'],
        }
    )
    return {
        'id': item.uuid,
        'name': item.name,
    }


def update_grade_policy(policy_id: str):
    item = get(p for p in GradePolicy if str(p.uuid) == policy_id)
    item.name = ''
    item.policy_conf = ''
    item.update_time = ''
    return True


def get_project_grade_report():
    pass


@db_session
def get_sprint_grade_report(sprint_id: str):
    pass


@db_session
def generate_grade_report(policy_id: str, sprint_id: str):
    """初始化 report"""
    report = {
        'project': {
            'bug_count_risk': 0,
            'prod_bug_risk': 0,
            'bug_found_rate': 0,
            'bug_density_risk': 0,
        },
        'sprint': {
            'bug_severity_rate': 0,
            'reopen_bug_rate': 0,
            'regression_bug_rate': 0,
            'previous_bug_rate': 0,
            'feature_found_bug_rate': 0,
            'improve_found_bug_rate': 0,
            'qamissed_bug_rate': 0,
            'rc_bug_risk': 0,
            'bug_growth_risk': 0,
            'bug_fix_rate': 0,
            'bug_fix_risk': 0,
            'bug_verify_rate': 0,
            'bug_verify_risk': 0,
            'feature_bug_risk': 0,
            # 'case_execution_rate': 0,
            # 'case_pass_rate': 0,
        },
    }
    """获取 issue 数据并进行指标计算 https://qualitysphere.gitee.io/images/point.png"""
    sprint = get(s for s in Sprint if str(s.uuid) == sprint_id)
    project = get(p for p in Project if p.uuid == sprint.project.uuid)
    # bugs in the Sprint ➗ average(bugs in all Sprints)
    bugs_in_the_sprint = get(i for i in IssueCaptureStaticProject if i.sprint.uuid == sprint.uuid).in_release['total']
    average_bugs_in_all_sprints = list()
    for item in select(i for i in IssueCaptureStaticProject if i.sprint.project.uuid == project.uuid):
        average_bugs_in_all_sprints.append(item.in_release['total'])
    report['project']['bug_count_risk'] = numpy.divide(
        bugs_in_the_sprint,
        numpy.mean(average_bugs_in_all_sprints)
    )
    # customer found bugs in the Sprint ➗ customer found bugs in the previous Sprint
    # team found bugs ➗ ( team found bugs + customer found bugs ) * 100%
    # ( the Sprint total bugs ➗ the Sprint new code lines ) ➗ ( previous Sprint total bugs ➗ previous Sprint new code lines)

    """创建 Sprint 评级报告"""
    item = GradeReportSprint(
        policy=get(p for p in GradePolicy if str(p.uuid) == policy_id),
        sprint=get(s for s in Sprint if str(s.uuid) == sprint_id),
        report=report
    )


if __name__ == '__main__':
    print(u'This is SERVICE for Grade')
