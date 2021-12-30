#!/bin/sh

pod_name=$(kubectl get pods -l app=$1 -ojsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}')

kubectl exec -it $pod_name -- /bin/bash