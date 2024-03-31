#!/bin/bash

# Allow user to update env.yaml
vimdiff "./ansible/env.yaml" "./ansible/env-template.yaml"

# Allow user to update inventory.yaml
vimdiff "./ansible/inventory.yaml" "./ansible/inventory-template.yaml"

# Run Ansible playbook
ansible-playbook -i ./ansible/inventory.yaml -e @./ansible/env.yaml -k -K ./ansible/update.yaml
