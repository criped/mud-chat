#!/bin/bash
set -e

cat >/etc/motd <<EOL
   Running MUD Server
EOL
cat /etc/motd

# wait until the database is built
wait-for-it.sh $DATABASEHOST:$DATABASEPORT -t 15 -- sleep 10
# Apply database schema changes
PYTHONUNBUFFERED=1 python manage.py migrate
# Load initial data
PYTHONUNBUFFERED=1 python manage.py loaddata world/fixtures/room.json
PYTHONUNBUFFERED=1 python manage.py loaddata world/fixtures/room_exit.json

# [production-adjustment] Runserver is only for local environments.
# For production we should deploy on some production ASGI server like daphne or uvicorn
# (https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/daphne/)
PYTHONUNBUFFERED=1 python manage.py runserver 9878
