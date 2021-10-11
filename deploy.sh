#!/usr/local/bin/bash

set -e
set -x

# push origin
git push origin master

# make sure tests pass
source venv/bin/activate
python manage.py test
deactivate

# pull and reload on server
ssh root@95.217.223.96 'cd /opt/apps/chaitin \
    && git pull \
    && source venv/bin/activate \
    && pip install -r requirements.txt \
    && python manage.py collectstatic --noinput \
    && python manage.py migrate \
    && touch /etc/uwsgi/vassals/chaitin.ini'
