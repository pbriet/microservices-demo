#!/bin/bash

echo "Please install K3D and make it available in your PATH"

echo "Then press ENTER: "
read dummy

mkdir -p local-persistent-data

k3d cluster create microservices --volume `pwd`/local-persistent-data:/persistent-data --registry-create k3d-microservices-registry:38597
kubectl config use-context k3d-microservices

echo ""
echo ""
echo ""
echo ""
echo "Add the following into your /etc/hosts :"
echo "127.0.0.1       k3d-microservices-registry"
echo ""
echo ""

echo "Please install DevSpace and make it available in your PATH"

echo ""
echo ""
echo "Then press ENTER: "
read dummy


kubectl create configmap rabbitmq-connection-credentials --from-literal=RABBITMQ_CONNECTION_STRING=amqp://rabbit:carrot@rabbitmq/%2F


echo ""
echo ""
echo ""
echo ""
echo "=== IMPORTANT NOTE ==="
echo ""
echo "This script will build & deploy everything locally"
echo "It will FAIL the first time, during syncing"
echo "The database migrations will also fail because the database is not ready yet"
echo ""
echo "Please wait a few minutes until the pods get stabilized, then run again the following command :"
echo "devspace deploy"
echo ""
echo "Then run 'devspace dev' & wait a little while, and a tab should be opened in your browser"
echo ""
echo ""

echo "press ENTER now to start everything: "
read dummy

devspace dev --force-build

