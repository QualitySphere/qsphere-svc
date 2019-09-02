#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pony.orm import Database, Required, db_session
import logging
import os


db = Database(
    provider='postgres',
    user=os.getenv('DB_USER') if os.getenv('DB_USER') else 'postgres',
    password=os.getenv('DB_PASSWORD') if os.getenv('DB_PORT') else 'password',
    host=os.getenv('DB_HOST') if os.getenv('DB_HOST') else '127.0.0.1',
    port=os.getenv('DB_PORT') if os.getenv('DB_PORT') else '5432',
    database='qap',
)
