# IN PROGRESS

# ansible-private-tls
Ansible role to create trusted self signed certificates for intra-cluster traffic

This role will create a self signed root CA and update the ca trust on all hosts to trust this CA.

In additon, this role will create multiple server and client certificates signed by the now trusted root CA.

Consideration, one of the hosts must be designated as the root. This Host will be used to generate all certificates

### Root Host variables
- `openssl_root` ansible host that will be used to generate and store certificats
- `openssl_base_dir` Directory where the certificate system will be store, default: `/etc/openssl`

### CA variables
- `openssl_ca_common_name` common name that will be used to identify this must not match, any server or client CN, default: `private-ca`
- `openssl_secret_ca_passphrase` passphrase used to secure CA signing requests
- `openssl_ca_cert_expiry` number of days the ca cert is valid for, default: `3650`




### Server Certificate Varaibales
 - `openssl_servers` [Optional] List of Servers that certificates should be generated for, common_name is the only required option, along with optional variables
```
 openssl_servers:
   - common_name: host1.example.com
     alt_DNS:
       - 10.0.0.1
       - "other.example.com"
     country: "US"
     state: "CA"
     locality: "San Jose"
     org: "miarec"
     org_unit: "devops"
     email: "ssl@example.com"
   - common_name: host2.example.com
     alt_DNS:
       - 10.0.0.50
       - "other.example.com"
     org: "miarec"
     org_unit: "sales"
     email: "ssl@example.com"

```
- `openssl_servers_cert_expiry` number of days the server certificates are valid for, default: `3650`


### Clients Certificate Varaibales


- `openssl_clients` [Optional] List of clients that certificates should be generated for, common_name is the only required option, along with optional variables
```
 openssl_clients:
   - common_name: apache_web_service
     country: "US"
     state: "CA"
     email: "ssl@example.com"
   - common_name: some.name@example.com
     org: "miarec"
     org_unit: "devops"
     email: "ssl@example.com"

```
- `openssl_clients_cert_expiry` number of days the client certificates are valid for, default: `3650`


## Updating certificates
The following variables can be supplied to regenerate certificats, this can be required if certificates have expired, or DNS names have been updated

- `openssl_ca_force_replace` When `true`;
    - existing CA certificate, key and CSR will be moved and regenerated,
    - exisitng client and server certificates will be moved and regenerated
    - CA trust will be updated on all hosts

- `openssl_servers_force_replace` When `true`, existing server certificates, keys and CSRs will be moved and regenerated
- `openssl_clients_force_replace` When `true`, existing client certificates, keys and CSRs will be moved and regenerated

Exisiting files will be moved to a new directory in the exising infrastructure for later reference

NOTE: this role generated new certificates, the new certs still need to be moved to the application using them and the services using them need to be restarted.


## Example Playbook



```
- name: Generate Private TLS infrastructure
  hosts:
    - all

  pre_tasks:
    - name: Define CA Root server and variables
      set_fact:
        openssl_root: "root_host"
        openssl_ca_common_name: my-ca
        openssl_servers:
          - common_name: host1
            alt_DNS:
                - host1.example.local
                - host1.example.com
          - common_name: host2.example.com

      set_fact:
        openssl_clients:
          - common_name: {{ item }}
            email: {{ item }}
      with_items:
        - foo.bar@example.com
        - bar.foo@example.com

  roles:
    - role: 'private-tls'
```

Result
```
user@host:/etc/openssl$ tree
.
├── ca
│   └── my-ca.key
│   └── my-ca.pem
├── server
│   └── host1
│       └── host1.csr
│       └── host1.key
│       └── host1.crt
│   └── host2.example.com
│       └── host2.example.com.csr
│       └── host2.example.com.key
│       └── host2.example.com.crt
├── clients
│   └── foo.bar@example.com
│       └── foo.bar@example.com.csr
│       └── foo.bar@example.com.key
│       └── foo.bar@example.com.crt
│   └── bar.foo@example.com
│       └── bar.foo@example.com.csr
│       └── bar.foo@example.com.key
│       └── bar.foo@example.com.crt

```