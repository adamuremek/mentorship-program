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
    # env.yaml doesn't exist so copy the template and open it in the editor
    cp "./ansible/env-template.yaml" "./ansible/env.yaml"
    ${EDITOR:-vi} "./ansible/env.yaml"
else
    # env.yaml exists so check if env-template.yaml exists
    if [ -f "./ansible/env-template.yaml" ]; then
        # env-template.yaml exists so use vimdiff to compare the two files and allow the user to update any changes
        $DIFF_COMMAND "./ansible/env.yaml" "./ansible/env-template.yaml"
    else
        # env-template.yaml doesn't exist so open env.yaml in the editor
        ${EDITOR:-vi} "./ansible/env.yaml"
    fi
fi

# Set inventory
# Check if inventory.yaml exists
if [ ! -f "./ansible/inventory.yaml" ]; then
    # inventory.yaml doesn't exist so copy the template and open it in the editor
    cp "./ansible/inventory-template.yaml" "./ansible/inventory.yaml"
    ${EDITOR:-vi} "./ansible/inventory.yaml"
else
    if [ -f "./ansible/inventory-template.yaml" ]; then
        # inventory-template.yaml exists so use vimdiff to compare the two files and allow the user to update any changes
        $DIFF_COMMAND "./ansible/inventory.yaml" "./ansible/inventory-template.yaml"
    else
        # inventory-template.yaml doesn't exist so open inventory.yaml in the editor
        ${EDITOR:-vi} "./ansible/inventory.yaml"
    fi
fi

# Install Ansible
sudo apt-get update
sudo apt-get install -y software-properties-common openssh-server sshpass
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible

# Install Python
sudo apt-get install -y python3-pip
sudo pip3 install --upgrade pip

# Install Ansible collections
ansible-galaxy collection install -r ./ansible/requirements.yaml

# Run Ansible playbook
export ANSIBLE_HOST_KEY_CHECKING=False && ansible-playbook -i ./ansible/inventory.yaml -e @./ansible/env.yaml -k -K ./ansible/master.yaml
