#!/bin/bash

oc apply -f order/deploy/db.yml
oc apply -f order/deploy/deployment.yml
oc apply -f order/deploy/job.yml
oc apply -f order/deploy/network.yml
oc process -f order/deploy/job.yml -p TAG=$CI_COMMIT_SHA | oc apply -f -