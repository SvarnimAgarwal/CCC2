#!/usr/bin/env bash
#
# Part of Assignment 2 - COMP90024 course at The University of Melbourne 
#
# Cluster and Cloud Computing - Team 43 
#
. ./openrc.sh; ansible-playbook -i hosts start_instances.yaml
