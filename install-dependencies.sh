#!/bin/bash

helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install rabbitmq bitnami/rabbitmq --values=rabbitmq-params.yml

# Manager UI
oc apply -f rabbitmq-manager.yml
