#!/bin/bash

oc apply -f kitchen/deploy/db.yml
oc apply -f kitchen/deploy/deployment.yml
oc apply -f kitchen/deploy/job.yml
oc apply -f kitchen/deploy/network.yml
oc process -f kitchen/deploy/job.yml -p TAG=$CI_COMMIT_SHA | oc apply -f -