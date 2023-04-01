#!/usr/bin/env python3

import ipaddress

from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import Optional, Union
from crypto import X25519

class User: ...
class Device: ...
class Network: ...
class VPN: ...
class Peer: ...

class NoAvailableAddressesError(Exception):
    pass

class PeerNotFoundError(Exception):
    pass

class InvalidAddressSpace(Exception):
    pass

class User:
    def __init__(self, name: str = None, devices: list[Device] = None) -> None:
        self.name = name
        self.devices = devices if devices is not None else []
        self.amount_of_devices = len(self.devices)

    def __repr__(self) -> str:
        return f"User(name='{self.name}', amount_of_devices={self.amount_of_devices})"

    def add_device(self, device: Device) -> None:
        self.devices.append(device)
        device.owner = self
        self.amount_of_devices = len(self.devices)

    def remove_device(self, device: Device) -> None:
        self.devices.remove(device)
        device.owner = None
        self.amount_of_devices = len(self.devices)

    def get_devices(self) -> list[Device]:
        return self.devices.copy()

    def find_device(self, devtype: str) -> Optional[Device]:
        for device in self.devices:
            if device.devtype == devtype:
                return device
        return None


class Device:
    def __init__(self, owner: User = None, devtype: str = None) -> None:
        self.owner = owner
        self.devtype = devtype

    def __repr__(self) -> str:
        return (
            f"Device(owner={self.owner}, "
            f"type='{self.devtype}')"
        )


class Peer(Device):
    def __init__(self, address=None, key=None, pub=None, name=None, vpn_membership=None, **kwargs):
        super().__init__(**kwargs)
        self.address = address
        if key is not None:
            self.key = key
            if pub is not None and pub != X25519.pubkey(key):
                raise ValueError("Public key does not match private key")
            self.pub = X25519.pubkey(key)
        elif pub is not None:
            self.pub = pub
            self.key = None
        else:
            self.key = X25519.genkey()
            self.pub = X25519.pubkey(self.key)
        self.name = name
        self.vpn_membership = vpn_membership

    def __repr__(self):
        return (
            f"Peer({super().__repr__()}, "
            f"vpn_membership='{self.vpn_membership}', key='{self.pub}')"
        )


class VPN:
    def __init__(self, name: str = None, address_space: str = None, amount_of_peers: int = 0) -> None:
        self.name = name
        self.address_space = address_space
        self.address_pool = []
        self.peers = []
        self.amount_of_available_addresses = 0
        self.amount_of_peers = amount_of_peers
        self._init_address_pool(address_space)

    def __repr__(self) -> str:
        return (
            f"VPN(name='{self.name}', "
            f"amount_of_peers='{self.amount_of_peers}', peers={self.peers}, "
            f"address_space='{self.address_space}')"
        )

    def _init_address_pool(self, address_space: str = None) -> None:
        if address_space is not None:
            try:
                self.address_space = ipaddress.ip_network(address_space)
                self.address_pool = list(self.address_space.hosts())
                self.amount_of_available_addresses = len(self.address_pool)
            except ValueError:
                raise ValueError("Invalid address space.")

    def _create_peer(self, **kwargs) -> Peer:
        if not self.address_pool:
            raise NoAvailableAddressesError("No available addresses in address pool.")
        peer_address = self.address_pool.pop(0)
        self.amount_of_available_addresses -= 1
        peer = Peer(address=ipaddress.ip_address(peer_address), **kwargs)
        self.peers.append(peer)
        return peer

    def create_peer(self, **kwargs) -> Optional[Peer]:
        try:
            peer = self._create_peer(**kwargs)
        except NoAvailableAddressesError:
            return None
        return peer

    def create_peers(self, amount_of_peers: int) -> None:
        if self.amount_of_available_addresses < amount_of_peers:
            plural_suffix = "es" if self.amount_of_available_addresses != 1 else ""
            verb_suffix = "is" if self.amount_of_available_addresses == 1 else "are"
            raise NoAvailableAddressesError(
                f"Not enough addresses in pool. Only {self.amount_of_available_addresses} "
                f"address{plural_suffix} {verb_suffix} available for allocation."
            )

        for _ in range(amount_of_peers):
            self._create_peer()

    def delete_peer(self, identifier: Union[str, IPv4Address, IPv6Address]) -> bool:
        for peer in self.peers:
            if peer.name == identifier or peer.address == identifier or peer.os == identifier:
                self.peers.remove(peer)
                self.address_pool.append(peer.address)
                self.amount_of_available_addresses += 1
                return True
        raise PeerNotFoundError(f"Peer with identifier {identifier} not found.")


def test_User():
    # Test User initialization
    user = User("Alice")
    assert user.name == "Alice"
    assert user.amount_of_devices == 0
    assert user.devices == []

    # Test add_device
    device = Device(devtype="laptop")
    user.add_device(device)
    assert user.amount_of_devices == 1
    assert user.devices == [device]
    assert device.owner == user

    # Test remove_device
    user.remove_device(device)
    assert user.amount_of_devices == 0
    assert user.devices == []
    assert device.owner is None

    # Test find_device
    device1 = Device(devtype="laptop")
    device2 = Device(devtype="phone")
    device3 = Device(devtype="tablet")
    user.add_device(device1)
    user.add_device(device2)
    user.add_device(device3)
    assert user.find_device("laptop") == device1
    assert user.find_device("phone") == device2
    assert user.find_device("tablet") == device3


def test_Peer():
    # Test initialization with key
    key = X25519.genkey()
    pub = X25519.pubkey(key)
    peer = Peer(key=key, name="Bob", vpn_membership=True)
    assert peer.key == key
    assert peer.pub == pub
    assert peer.name == "Bob"
    assert peer.vpn_membership is True

    # Test initialization with pub
    pub = X25519.genkey()
    peer = Peer(pub=pub, name="Bob", vpn_membership=False)
    assert peer.key is None
    assert peer.pub == pub
    assert peer.name == "Bob"
    assert peer.vpn_membership is False

    # Test initialization without key or pub
    peer = Peer(name="Bob", vpn_membership=True)
    assert peer.key is not None
    assert peer.pub == X25519.pubkey(peer.key)
    assert peer.name == "Bob"
    assert peer.vpn_membership is True

def test_all():
    test_User()
    test_Peer()

if __name__ == '__main__':
    test_all()