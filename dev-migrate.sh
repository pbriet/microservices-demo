#!/bin/bash

docker-compose run order python manage.py migrate
docker-compose run kitchen python manage.py migrate
docker-compose run delivery python manage.py migrate