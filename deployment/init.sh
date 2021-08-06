#!/bin/bash
set -e

cat >/etc/motd <<EOL
   Running MUD Server
EOL
cat /etc/motd

PYTHONUNBUFFERED=1 python main/server.py
