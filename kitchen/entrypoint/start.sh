#!/bin/bash

set -ex

echo "[Kitchen] Start watchmedo"

# Start celery in bg with watchmedo
if [[ "$RUN_CELERY" == "true" ]]
then
  watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery --beat -A kitchen.celery worker --loglevel=info --schedule=/tmp/celerybeat-schedule > /dev/stdout 2>&1 &
fi

# Run command

echo "[Kitchen] Executing $@"
exec "$@"