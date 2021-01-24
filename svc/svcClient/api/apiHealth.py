#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import json


def health_check():
    return {
        'status': 'healthy'
    }, 200


def host_check():
    host_status_file = os.path.join('svcClient', 'specs', 'machine-status.json')
    with open(host_status_file, 'r') as f:
        results = f.read()
    return json.loads(results), 200

