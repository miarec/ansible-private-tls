# IN PROGRESS

# ansible-private-tls
Ansible role to create trusted self signed certificates for intra-cluster traffic


'server'
> Create a Root CA

> Creaate a server certificate


on all 'clients'
add root ca to anshors / update ca trust 'client'




hosts: all
set_fact:
    server: db.example.com
roles: this role



tasks/main.yml
    include: create CA
        delegate_to: "{{ server }}"