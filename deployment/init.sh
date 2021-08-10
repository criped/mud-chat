#!/bin/bash
set -e

cat >/etc/motd <<EOL
   Running MUD Server
EOL
cat /etc/motd

PYTHONUNBUFFERED=1 python manage.py migrate
# Runserver is only for local environments. For production we should deploy on some production ASGI server
# like daphne or uvicorn (https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/daphne/)
PYTHONUNBUFFERED=1 python manage.py runserver 9878
