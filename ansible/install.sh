#!/bin/bash

# Set environment variables
cp ./ansible/env-template.yaml ./ansible/env.yaml
${EDITOR:-vi} ./ansible/env.yaml

# Set inventory
cp ./ansible/inventory-template.yaml ./ansible/inventory.yaml
${EDITOR:-vi} ./ansible/inventory.yaml

# Install Ansible
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible

# Install Python
sudo apt-get install -y python3-pip
sudo pip3 install --upgrade pip

# Install Ansible collections
ansible-galaxy collection install -r ./ansible/requirements.yaml

# Run Ansible playbook
ansible-playbook -i ./ansible/inventory.yaml -e @./ansible/env.yaml -k -K ./ansible/master.yaml
