#!/bin/bash
source .env
python3 .compose/compose.py -d "$@"
docker compose exec $SERVICE /bin/bash
exec bash
