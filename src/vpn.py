import ipaddress
from .pool import Pool

class VPN:
    class Peer:
        def __init__(self, address=None, endpoint=False, is_router=False):
            self.address = ipaddress.IPv4Address(address)
            self.endpoint = None
            self.is_router = is_router
            if endpoint:
                self.endpoint = ipaddress.IPv4Address(endpoint)
                self.is_router = True

        def __repr__(self):
            if self.is_router:
                return f"Router(endpoint='{self.endpoint}', address='{self.address}')"
            else:
                return f"Peer(address='{self.address}')"

    class Router(Peer):
        def __init__(self, address=None, endpoint=False):
            super().__init__(address, endpoint, True)
            self.routes = []

        def add_route(self, destination, gateway):
            destination = ipaddress.IPv4Network(destination)
            gateway = ipaddress.IPv4Address(gateway)
            self.routes.append((destination, gateway))

        def remove_route(self, destination, gateway):
            destination = ipaddress.IPv4Network(destination)
            gateway = ipaddress.IPv4Address(gateway)
            self.routes.remove((destination, gateway))

    def __init__(self, address_space, endpoint=False):
        self.pool = Pool(address_space)
        self.peers = []
        if endpoint:
            self.endpoint = self.add_peer(endpoint=endpoint)

    def __repr__(self):
        return f"VPN(peers={repr(self.peers)}, pool={repr(self.pool)})"

    def add_peer(self, address=None, endpoint=False):
        if address is not None:
            address = ipaddress.IPv4Address(address)
            if address in self.pool.allocated_addresses:
                raise ValueError(f"Error: Address {address} is already allocated.")
        peer = self.Peer(self.pool.allocate_address(address), endpoint=endpoint)
        self.peers.append(peer)
        return peer

    def remove_peer(self, address=None):
        try:
            if address is None:
                peer = self.peers.pop()
                self.pool.unallocate_address(peer.address)
            else:
                address = ipaddress.IPv4Address(address)
                if address not in self.pool.allocated_addresses:
                    raise ValueError(f"Error: Address {address} is not allocated.")
                for peer in self.peers:
                    if peer.address == address:
                        self.pool.unallocate_address(address)
                        self.peers.remove(peer)
                        break
        except (ValueError, IndexError) as e:
            raise e
