#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pony.orm import Database
import os


db = Database(
    provider='postgres',
    user=os.getenv('PG_USER') or 'postgres',
    password=os.getenv('PG_PASS') or 'password',
    host=os.getenv('PG_HOST') or '127.0.0.1',
    port=os.getenv('PG_PORT') or '5432',
    database='qsphere'
)
