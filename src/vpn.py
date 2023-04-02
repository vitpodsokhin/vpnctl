import ipaddress
import json
from pool import Pool

class VPN:
    class Peer:
        def __init__(self, address=None, endpoint=False, is_router=False):
            self.address = ipaddress.IPv4Address(address)
            self.is_router = is_router
            self.endpoint = None
            if endpoint:
                self.endpoint = ipaddress.IPv4Address(endpoint)
                self.is_router = True

        def __repr__(self):
            if self.is_router:
                return f"Router(address='{self.address}', endpoint='{self.endpoint}')"
            else:
                return f"Peer(address='{self.address}')"

    class Router(Peer):
        def __init__(self, vpn, address=None, endpoint=False):
            super().__init__(address, endpoint, True)
            self.vpn = vpn

    def __init__(self, address_space, endpoint=False):
        self.pool = Pool(address_space)
        self.network = self.pool.exploded
        self.endpoints = []
        self.peers = []
        if endpoint:
            self.endpoints.append(self.add_peer(endpoint=endpoint).endpoint.exploded)

    def __repr__(self):
        return f"VPN(network={self.network}, endpoints={[self.endpoints]}, peers={repr(self.peers)}, left_in_pool={len(self.pool.unallocated_addresses)})"

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

    def to_json(self):
        json_dict = {
            "peers": [],
            "pool": {
                "address_space": self.pool.exploded,
                "unallocated_addresses_amount": len(self.pool.unallocated_addresses)
            }
        }
        for peer in self.peers:
            json_peer = {
                "address": str(peer.address),
                "endpoint": str(peer.endpoint),
                "is_router": peer.is_router
            }
            json_dict["peers"].append(json_peer)
        return json.dumps(json_dict)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        address_space = ipaddress.IPv4Network(json_dict["pool"]["address_space"])
        vpn = cls(address_space)
        for peer_dict in json_dict["peers"]:
            address = ipaddress.IPv4Address(peer_dict["address"])
            endpoint = peer_dict["endpoint"]
            is_router = peer_dict["is_router"]
            if is_router:
                #TODO try to fix an error here, please
                peer = VPN.Router(vpn, address=address, endpoint=endpoint)
            else:
                peer = VPN.Peer(address=address, endpoint=None)
            vpn.add_peer(peer.address, peer.endpoint)
        return vpn
