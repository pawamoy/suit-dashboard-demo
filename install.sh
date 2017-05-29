#!/usr/bin/env bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
pushd demo
./manage.py migrate
./manage.py shell <<EOF
from django.contrib.auth.models import User
User.objects.create_superuser(username='$USER', email='', password='admin_password')
EOF
./manage.py loaddata ../user_fixture.json
popd
./run.sh
