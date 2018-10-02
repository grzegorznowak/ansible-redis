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


@pytest.mark.parametrize('svc', [
    'redis-cache0', 'redis-cache1'
])
def test_svc(host, svc):
    service = host.service(svc)

    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize('svc', [
    'redis-server'
])
def test_disabled_svc(host, svc):
    service = host.service(svc)

    assert not service.is_running
    assert not service.is_enabled


@pytest.mark.parametrize('port', [
    '6379', '6380'
])
def test_ports(host, port):
    assert host.socket("tcp://127.0.0.1:{}".format(port)).is_listening


@pytest.mark.parametrize('port', [
    '6379', '6380'
])
def test_persistence(host, port):

    # @see https://stackoverflow.com/a/7021653
    cmd = host.run('{ echo "SAVE";  sleep 1; } | telnet 127.0.0.1 ' + port)
    assert "OK" in cmd.stdout
    assert "ERR" not in cmd.stdout


@pytest.mark.parametrize('port', [
    '6379', '6380'
])
def test_store(host, port):

    cmd = host.run(
        '{ echo "SET testkey \"TEST\"";  sleep 1; } | telnet 127.0.0.1 '
        + port)
    assert "OK" in cmd.stdout
    assert "ERR" not in cmd.stdout

    cmd = host.run(
        '{ echo "GET testkey";  sleep 1; } | telnet 127.0.0.1 '
        + port)
    assert "TEST" in cmd.stdout
    assert "ERR" not in cmd.stdout
