#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from clientJira.services import jiraSprint


def list_sprints():
    return jiraSprint.list_sprints()


def get_sprint(sprint_id):
    return jiraSprint.get_sprint(sprint_id)


def post_sprint(body):
    return jiraSprint.create_sprint(body)


def put_sprint(sprint_id, body):
    return jiraSprint.update_sprint(sprint_id, body)


def delete_sprint(sprint_id):
    return jiraSprint.delete_sprint(sprint_id)


def disable_sprint(sprint_id):
    return jiraSprint.disable_sprint(sprint_id)


def active_sprint(sprint_id):
    return jiraSprint.active_sprint(sprint_id)

