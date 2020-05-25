#!/bin/sh
set -ex
netstat -tlnup | grep nginx
