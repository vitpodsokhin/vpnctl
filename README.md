# VPN address space manager

*   WARNING: is under early heavy development. Use it on your own risk.

This project is a Python implementation of a VPN address space manager that allows the allocation and deallocation of addresses within an IP address space.

## Features

The VPN Manager consists of two main classes:

1.   `` Pool ``: A class for managing IP addresses allocated to network peers.
2.   `` VPN ``: A class for managing VPN peers and their routes.

The features of each class are described below.

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

### VPN

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

## TODO:

*   Implement a method to connect a peer to the VPN.
*   Implement a method to disconnect a peer from the VPN.
*   Implement a method to list all peers and their status (connected or not).
*   Implement error handling for cases where the VPN pool runs out of addresses to allocate.
*   Add logging functionality to track VPN usage and errors.
*   Implement unit tests to ensure the correct behavior of the VPN and its components.



