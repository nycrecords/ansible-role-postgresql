import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_postgresql_installed(host):
    postgresql = host.package("rh-postgresql96")

    assert postgresql.is_installed


def test_postgres_listening(host):
    socket = host.socket("tcp://127.0.0.1:5432")

    assert socket.is_listening


def test_postgresql_config_exists(host):
    postgresql_conf = host.file(
        "/var/opt/rh/rh-postgresql96/lib/pgsql/data/postgresql.conf"
    )

    with host.sudo():
        assert postgresql_conf.exists
        assert postgresql_conf.is_file
        assert postgresql_conf.user == "postgres"
        assert postgresql_conf.group == "postgres"


def test_hba_config(host):
    pg_hba = host.file("/var/opt/rh/rh-postgresql96/lib/pgsql/data/pg_hba.conf")

    with host.sudo():
        jdoe_example = pg_hba.contains("host example jdoe 127.0.0.1/32   md5")

        assert jdoe_example
        assert pg_hba.exists
        assert pg_hba.is_file
        assert pg_hba.user == "postgres"
        assert pg_hba.group == "postgres"
