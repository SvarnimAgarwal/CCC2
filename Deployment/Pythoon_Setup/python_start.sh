#!/usr/bin/env bash
ansible-galaxy collection install openstack.could:2.0.0
./openrc.sh; ansible-playbook -i hosts python_start.yaml
