#!/usr/local/bin/bash

set -e
set -x

# make sure linting checks pass
make lint

# static
python manage.py collectstatic --noinput

# make sure tests pass
python manage.py test

# push origin
git push origin master
git push github master

# pull and reload on server
ssh root@95.217.223.96 'cd /opt/apps/chaitin \
    && git pull \
    && source venv/bin/activate \
    && pip install -r requirements.txt \
    && python manage.py collectstatic --noinput \
    && python manage.py migrate \
    && touch /etc/uwsgi/vassals/chaitin.ini'
