import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_directories(host):
    dirs = [
        "/etc/openssl",
        "/etc/openssl/ca",
        "/etc/openssl/servers",
        "/etc/openssl/servers/server.example.com",
        "/etc/openssl/clients",
        "/etc/openssl/clients/client@example.com"
    ]

    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists

def test_files(host):
    files = [
        "/etc/openssl/ca/private-ca.pem",
        "/etc/openssl/ca/private-ca.key",
        "/etc/openssl/servers/server.example.com/server.example.com.cnf",
        "/etc/openssl/servers/server.example.com/server.example.com.csr",
        "/etc/openssl/servers/server.example.com/server.example.com.key",
        "/etc/openssl/servers/server.example.com/server.example.com.crt",
        "/etc/openssl/clients/client@example.com/client@example.com.cnf",
        "/etc/openssl/clients/client@example.com/client@example.com.csr",
        "/etc/openssl/clients/client@example.com/client@example.com.key",
        "/etc/openssl/clients/client@example.com/client@example.com.crt"
    ]

    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_cert(host):
    certs = [
        "/etc/openssl/servers/server.example.com/server.example.com.crt",
        "/etc/openssl/clients/client@example.com/client@example.com.crt"
    ]

    for cert in certs:
        cmd = host.run ("openssl verify -CAfile /etc/openssl/ca/private-ca.pem {}".format(cert))
        assert cmd.rc == 0

