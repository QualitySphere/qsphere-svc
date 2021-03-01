#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from services import svcUser
from utils.exceptionHandle import DefaultError


def login(body):
    """
    PUT /api/user/login
    :param body:
    :return:
    """
    try:
        return {
            'title': 'Succeed to login',
            'detail': svcUser.login(body)
        }, 200
    except Exception as e:
        raise DefaultError(title='Failed to login', detail=str(e))
