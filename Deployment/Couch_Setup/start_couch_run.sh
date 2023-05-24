#!/usr/bin/env bash
#
# Part of Assignment 2 - COMP90024 course at The University of Melbourne 
#
# Cluster and Cloud Computing - Team 43 
#
ansible-galaxy collection install openstack.could:2.0.0
. ./openrc.sh; ansible-playbook -i hosts start_couch.yaml
