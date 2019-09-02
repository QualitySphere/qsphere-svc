#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from clientJira.services import jiraProject


def list_projects(path):
    return jiraProject.list_project(path.get('connectionId'))


def get_project(path):
    return jiraProject.get_project(path.get('projectId'))


def post_project(body):
    return jiraProject.create_project(body)


def put_project(body):
    pass


def delete_project():
    pass

