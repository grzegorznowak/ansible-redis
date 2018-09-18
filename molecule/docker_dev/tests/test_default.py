import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('pkg', [
    'redis-server'
])
def test_pkg(host, pkg):
    package = host.package(pkg)

    assert package.is_installed


@pytest.mark.parametrize('port', [
    '6379', '6380'
])
def test_ports(host, port):
    assert host.socket("tcp://127.0.0.1:{}".format(port)).is_listening
