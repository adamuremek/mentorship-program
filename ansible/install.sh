#!/bin/bash

# Check if vimdiff is available
if command -v vimdiff &> /dev/null; then
    DIFF_COMMAND="vimdiff"
else
    DIFF_COMMAND="${EDITOR:-vi}"
fi

# Set environment
# Check if env.yaml exists
if [ ! -f "./ansible/env.yaml" ]; then
    cp "./ansible/env-template.yaml" "./ansible/env.yaml"
    ${EDITOR:-vi} "./ansible/env.yaml"
else
    if [ -f "./ansible/env-template.yaml" ]; then
        $DIFF_COMMAND "./ansible/env.yaml" "./ansible/env-template.yaml"
    else
        ${EDITOR:-vi} "./ansible/env.yaml"
    fi
fi

# Set inventory
# Check if inventory.yaml exists
if [ ! -f "./ansible/inventory.yaml" ]; then
    cp "./ansible/inventory-template.yaml" "./ansible/inventory.yaml"
    ${EDITOR:-vi} "./ansible/inventory.yaml"
else
    if [ -f "./ansible/inventory-template.yaml" ]; then
        $DIFF_COMMAND "./ansible/inventory.yaml" "./ansible/inventory-template.yaml"
    else
        ${EDITOR:-vi} "./ansible/inventory.yaml"
    fi
fi

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
