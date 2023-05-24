#!/usr/bin/env bash
ansible-galaxy collection install openstack.could:2.0.0
./unimelb-comp90024-2023-grp-43-openrc.sh; ansible-playbook -i hosts setup_harvestor_worker.yaml