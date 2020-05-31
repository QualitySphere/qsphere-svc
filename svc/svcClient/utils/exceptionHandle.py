#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from connexion import ProblemException


class DefaultError(ProblemException):
    def __init__(self, type='DefaultError', title='Unknown Error', detail='', status=400, **kwargs):
        super().__init__(type=type, title=title, detail=detail, status=status, **kwargs)


if __name__ == '__main__':
    print(u'This is a service of Exception Handler')
