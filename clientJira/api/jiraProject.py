#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from clientJira.services import jiraProject


def list_projects():
    return jiraProject.list_project()


def get_project(project_id):
    return jiraProject.get_project(project_id)


def post_project(body):
    return jiraProject.create_project(body)


def put_project(body):
    pass


def delete_project():
    pass

