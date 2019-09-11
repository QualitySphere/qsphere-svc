#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from clientJira.services import jiraSprint


def list_sprints():
    return jiraSprint.list_sprint()


def get_sprint(sprint_id):
    return jiraSprint.get_sprint(sprint_id)


def post_sprint(body):
    return jiraSprint.create_sprint(body)


def put_sprint(body):
    pass


def delete_sprint():
    pass

