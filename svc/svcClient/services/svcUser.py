#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


def login(body: dict):
    """
    Login
    :param body:
    :return:
    """
    assert body.get('username') == 'admin', u'Username is wrong: %s' % body.get('username')
    assert body.get('password') == os.getenv('SVC_PASS'), u'Password is wrong'
    return True


if __name__ == '__main__':
    print(u'This is SERVICE for user')
