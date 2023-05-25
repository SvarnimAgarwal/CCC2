#!/bin/bash
sudo docker run --restart=always --name couchdb -v /home/ubuntu/couch-mount:/opt/couchdb/data -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=admin -e NODENAME=172.26.135.88 -p 5984:5984 -p 5986:5986 -p 4369:4369 -p 9100-9200:9100-9200 -d ibmcom/couchdb:3.2.1
