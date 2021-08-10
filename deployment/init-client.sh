#!/bin/bash
set -e

cat >/etc/motd <<EOL
   Running MUD Client
EOL
cat /etc/motd

PYTHONUNBUFFERED=1 python client.py
