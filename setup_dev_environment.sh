#!/bin/bash

echo "Please install K3D and make it available in your PATH"

echo "The press ENTER: "
read dummy

mkdir -p local-persistent-data

k3d cluster create microservices --volume `pwd`/local-persistent-data:/persistent-data --registry-create k3d-microservices-registry:38597
kubectl config use-context k3d-microservices

echo "Add the following into your /etc/hosts :"
echo "127.0.0.1       k3d-microservices-registry"

echo "Please install DevSpace and make it available in your PATH"

echo "The press ENTER: "
read dummy


kubectl create configmap rabbitmq-connection-credentials --from-literal=RABBITMQ_CONNECTION_STRING=amqp://rabbit:carrot@rabbitmq/%2F

devspace dev --force-build



