# VPN address space manager

*   WARNING: is under early heavy development. Use it on your own risk.

This project is a Python implementation of a VPN address space manager that allows the allocation and deallocation of addresses within an IP address space.

## Features

The VPN Manager consists of two main classes:

1.   `` VPN ``: A class for managing VPN peers and their routes.
2.   `` Pool ``: A class for managing IP addresses allocated to network peers.

The features of each class are described below.

### VPN

This code defines a `` VPN `` class which has two nested classes: `` Peer `` and `` Router ``.

##### The `` Peer `` class represents a network peer and has the following attributes:

*   `` address ``: An IPv4 address object representing the IP address of the peer.
*   `` is_router ``: A boolean flag indicating whether the peer is a router or not.
*   `` endpoint ``: An IPv4 address object representing the endpoint of the peer, if it is a router.

The `` Peer `` class also has a `` __repr__ `` method that returns a string representation of the object.

##### The `` Router `` class extends the `` Peer `` class and represents a network router. It has an additional attribute:

*   `` vpn ``: A reference to the VPN object that the router belongs to.

#### The `` VPN `` class has the following attributes:

*   `` pool ``: A `` Pool `` object representing the address space of the VPN.
*   `` network ``: A string representing the network address of the VPN.
*   `` endpoints ``: A list of strings representing the endpoint addresses of the routers in the VPN.
*   `` peers ``: A list of `` Peer `` objects representing all the peers in the VPN.

The `` VPN `` class has the following methods:

*   `` add_peer ``: Adds a new peer to the VPN. If an address is specified, it is used as the IP address of the peer. Otherwise, a new IP address is allocated from the VPN's address pool. If `` endpoint `` is specified, a new router is added with the specified endpoint. Returns the new `` Peer `` or `` Router `` object.
*   `` remove_peer ``: Removes a peer from the VPN. If an address is specified, the peer with the specified address is removed. Otherwise, the last peer in the list is removed. Raises a `` ValueError `` if the address is not found or the list is empty.
*   `` to_json ``: Returns a JSON string representation of the VPN object.
*   `` from_json ``: Returns a new VPN object from a JSON string representation.


The `` VPN `` class manages VPN peers and their routes. It uses the `` Pool `` class to allocate IP addresses to VPN peers.

#### Initialization

The `` VPN `` class can be initialized with the following arguments:

*   `` address_space ``: An `` IPv4Network `` object representing the network address space.
*   `` endpoint `` (optional): An accessible IP address to be allocated to the VPN endpoint.

#### Methods

The `` VPN `` class provides the following methods:

*   `` add_peer(address=None, endpoint=False) ``: Adds a VPN peer to the network. If `` address `` is provided, it will be used as the IP address of the peer. If `` endpoint `` is set to `` True ``, the peer will be treated as a router and an IP address will be allocated to it as well.
*   `` remove_peer(address=None) ``: Removes a VPN peer from the network. If `` address `` is not provided, the last added peer will be removed.
*   `` Router ``: A subclass of `` Peer `` representing a VPN router.
*   `` Peer ``: A class representing a VPN peer.

### Pool

The `` Pool `` class is a subclass of the `` IPv4Network `` class from the `` ipaddress `` module. It manages IP addresses allocated to network peers.

#### Initialization

The `` Pool `` class can be initialized with the following arguments:

*   `` address_space ``: An `` IPv4Network `` object representing the network address space.
*   `` hosts_num `` (optional): An integer representing the number of hosts to be allocated. If set to 0 (default), all available hosts will be allocated.

#### Methods

The `` Pool `` class provides the following methods:

*   `` allocate_address(address=None) ``: Allocates an IP address from the pool. If `` address `` is not provided, the first unallocated IP address will be allocated.
*   `` unallocate_address(address=None) ``: Frees an allocated IP address. If `` address `` is not provided, the last allocated IP address will be freed.

## TODO:

*   Cover objects initialization, modification and regeneration with unittests.
