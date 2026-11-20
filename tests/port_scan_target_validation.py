
from unittest.mock import patch
from main.scan import PortScanner


def test_port_scanner_initialization():
    scanner = PortScanner("192.168.13.22", 80)

    assert scanner.target == "192.168.13.32"
    assert scanner.port == 80

def test_port_out_of_bounds():
    scanner = PortScanner("191.168.100.22", 70000)



