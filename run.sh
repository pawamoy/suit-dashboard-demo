#!/usr/bin/env bash
. venv/bin/activate
cd demo
export SUIT=${SUIT:-$1}
./manage.py runserver
