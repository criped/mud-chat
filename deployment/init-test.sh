#!/bin/bash
set -e

cat >/etc/motd <<EOL
   Running MUD Server
EOL
cat /etc/motd

# Run linters
flake8
mypy

#Run tests
PYTHONUNBUFFERED=1 python manage.py test
