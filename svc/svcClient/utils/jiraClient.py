#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from jira import JIRA
import logging


class JiraSession(object):
    def __init__(self, server, account, password, verify=True):
        """
        Init Jira Session
        :param server:
        :param account:
        :param password:
        :param verify:
        """
        self.__server = server
        self.__account = account
        self.__password = password
        self.__jira_opts = {
            'server': self.__server,
            'verify': verify,
        }
        self.__session = JIRA(self.__jira_opts, basic_auth=(self.__account, self.__password))

    def __enter__(self):
        assert self.__session.current_user() == self.__account
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.close()

    def get_user(self):
        """
        Get jira user
        :return:
        """
        logging.info(u'Get JIRA Current User')
        return self.__session.current_user()

    def search_issues(self, jql):
        """
        Search issues via JQL
        :param jql:
        :return:
        """
        logging.info(u'JIRA Search: %s' % jql)
        return self.__session.search_issues(jql_str=jql, maxResults=128, json_result=True)

    # def get_issue_count(self, jql: str, issue_summary: dict, issue_key: str):
    #     """
    #     Search issues via JQL and return count
    #     :param jql:
    #     :param issue_summary:
    #     :param issue_key:
    #     :return:
    #     """
    #     logging.info(u'JIRA Issue Count: %s' % jql)
    #     issue_summary[issue_key] = int(self.search_issues(jql).get('total'))
    #     return True

    def get_projects(self):
        """
        Get jira projects
        :return: <key, name, id>
        """
        logging.info(u'Get JIRA Projects')
        return self.__session.projects()

    def get_sprints(self):
        """
        Get jira sprints
        :return: <name, id>
        """
        logging.info(u'Get JIRA Sprints')
        jira_sprints = list()
        for board in self.__session.boards():
            _sprints = self.__session.sprints(board.id)
            jira_sprints = jira_sprints + _sprints
        return jira_sprints

    def get_issue_fields(self):
        """
        Get jira fields
        :return: [{'name':'','id':''}]
        """
        logging.info(u'Get JIRA Fields')
        _fields = list()
        for _field in self.__session.fields():
            _fields.append({
                'name': _field['name'],
                'id': _field['id']
            })
        return _fields

    def get_issue_types(self):
        """
        Get jira issue types
        :return: <name, id>
        """
        logging.info(u'Get JIRA Issue Types')
        return self.__session.issue_types()

    def get_issue_statuses(self):
        """
        Get issue statuses
        :return: <name, id>
        """
        logging.info(u'Get JIRA Issue Statuses')
        return self.__session.statuses()

    def get_project_versions(self, pid: str):
        """
        Get project versions
        :param pid:
        :return: [<name, id>]
        """
        logging.info(u'Get JIRA Project %s Versions' % pid)
        return self.__session.project_versions(project=pid)


if __name__ == '__main__':
    print(u'This is a service of JIRA connection')
