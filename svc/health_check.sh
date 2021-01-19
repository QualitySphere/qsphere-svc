#!/bin/sh
set -ex
python3 -c "import requests; print(requests.get('http://localhost/api/status').status_code)" | grep 200
