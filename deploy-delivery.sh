#!/bin/bash

oc apply -f delivery/deploy/db.yml
oc apply -f delivery/deploy/deployment.yml
oc apply -f delivery/deploy/job.yml
oc apply -f delivery/deploy/network.yml
oc process -f delivery/deploy/job.yml -p TAG=$CI_COMMIT_SHA | oc apply -f -