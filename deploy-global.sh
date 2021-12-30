#!/bin/bash

oc apply -f global-deploy.yml

# Enable Openshift image streams
oc set image-lookup order
oc set image-lookup payment
oc set image-lookup kitchen
oc set image-lookup delivery