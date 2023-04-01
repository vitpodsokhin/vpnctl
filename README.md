# VPN address space manager

WARNING: is under early heavy development. Use it on your own risk.
This project is a Python implementation of a VPN address space manager that allows the allocation and deallocation of addresses within an IP address space.

## Pool Class

The `` Pool `` class represents an IP address space and provides methods for allocating and deallocating IP addresses. It is a subclass of the `` IPv4Network `` class from the `` ipaddress `` module. It initializes with an `` address_space `` argument, which is an instance of the `` IPv4Network `` class, and an optional `` hosts_num `` argument, which represents the number of hosts that should be allocated on initialization. If `` hosts_num `` is not provided, all hosts within the `` address_space `` are considered unallocated.

The following methods are available:

*   `` allocate_address() ``: Allocates an IP address from the pool.
*   `` unallocate_address() ``: Deallocates an IP address and returns it to the pool.
*   `` _sort_spaces() ``: Internal method to sort allocated and unallocated IP address spaces.
*   `` __repr__() ``: Returns a string representation of the `` Pool `` object, including the total number of hosts, the number of unallocated hosts, and the lists of allocated and unallocated IP addresses.

## VPN Class

The `` VPN `` class provides a high-level interface for managing a pool of IP addresses for a VPN. It uses the `` Pool `` class to allocate and deallocate IP addresses for peers.

The following methods are available:

*   `` add_peer() ``: Adds a new peer to the VPN by allocating an IP address from the pool.
*   `` remove_peer(address) ``: Removes a peer from the VPN by deallocating its IP address and removing it from the list of peers.
*   `` __repr__() ``: Returns a string representation of the `` VPN `` object, including the VPN name, the address space managed by the VPN, and the list of allocated and unallocated IP addresses.

Attributes:

*   `` name `` (str): The name of the VPN.
*   `` address_space `` (str): The IP address space used by the VPN.
*   `` address_pool `` (list): A list of available IP addresses for use by devices connected to the VPN.
*   `` routers `` (list): A list of `` Router `` objects representing the routers used by the VPN.
*   `` users `` (list): A list of `` User `` objects representing the users connected to the VPN.

### Class `` Router ``

Represents a router in the VPN.

Attributes:

*   `` name `` (str): The name of the router.
*   `` peer `` (`` Peer ``): The peer object representing the router's connection to the VPN.
*   `` endpoint `` (`` tuple ``): A tuple of the form `` (ip_address, port) `` representing the endpoint of the router.

### Class `` User ``

Represents a user connected to the VPN.

Attributes:

*   `` name `` (str): The name of the user.
*   `` address_pool `` (list): A list of available IP addresses for use by the user's devices.
*   `` devices `` (list): A list of `` Device `` objects representing the user's devices.

### Class `` Device ``

Represents a device used by a user in the VPN.

Attributes:

*   `` name `` (str): The name of the device.
*   `` owner `` (`` User ``): The `` User `` object representing the device's owner.
*   `` peer `` (`` Peer ``): The peer object representing the device's connection to the VPN.

### Class `` Peer ``

Represents a peer connection in the VPN.

Attributes:

*   `` keys `` (str): The encrypted keys used for the connection.
*   `` addresses `` (list): A list of IP addresses used for the connection.

TODO:

*   Implement a method to connect a peer to the VPN.
*   Implement a method to disconnect a peer from the VPN.
*   Implement a method to list all peers and their status (connected or not).
*   Implement error handling for cases where the VPN pool runs out of addresses to allocate.
*   Add logging functionality to track VPN usage and errors.
*   Implement unit tests to ensure the correct behavior of the VPN and its components.