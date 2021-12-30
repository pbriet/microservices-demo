# Microservices architecture demo

A demo that shows how a real microservices architecture should be :
* Services splitted by domain, with their own databases
* Message brokers with asynchronous messaging
* SAGAs for cross-domain operations


## Connectivity

This demo covers the following issues :

* Potential duplication of broker messages  (in some case of broker crash)
* The atomicity of bdd commits + event messaging
* Ensuring ACD thanks to the Saga pattern


## Limitations

This repo should _theorically_ be splitted. There shouldn't be more than **1** microservice in each Git repo, to ensure loose coupling and teams autonomy.

The centralization of everything in one repo is only justified here in the purpose of a demo.
