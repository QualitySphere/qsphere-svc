#!/bin/sh
set -ex
curl -sv http://localhost:6001/api/jira/connection 2>&1 | grep '^< HTTP' | grep '200 OK'