#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pony.orm import Database
import os


db = Database(
    provider='postgres',
    user=os.getenv('PG_USER') if os.getenv('PG_USER') else 'postgres',
    password=os.getenv('PG_PASSWORD') if os.getenv('PG_PORT') else 'password',
    host=os.getenv('PG_SERVER') if os.getenv('PG_SERVER') else '127.0.0.1',
    port=os.getenv('PG_PORT') if os.getenv('PG_PORT') else '5432',
    database='qap',
)
