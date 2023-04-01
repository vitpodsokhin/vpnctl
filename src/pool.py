import ipaddress

class Pool(ipaddress.IPv4Network):
    def __init__(self, address_space: ipaddress.IPv4Network, hosts_num: int = 0, *args, **kwargs):
        try:
            super().__init__(address_space, *args, **kwargs)
            self.hosts_list = list(self.hosts())
            if hosts_num == 0:
                self.unallocated_addresses = self.hosts_list[:]
                self.allocated_addresses = []
            elif hosts_num <= len(list(self.hosts())):
                self.allocated_addresses = self.hosts_list[:hosts_num]
                self.unallocated_addresses = self.hosts_list[hosts_num:]
            else:
                raise ValueError(f"Error: The number of requested hosts ({hosts_num}) exceeds the number of available hosts in the address space ({len(self.hosts_list)}).")
        except ValueError as e:
            raise e

    def __repr__(self) -> str:
        try:
            return (
                f"Pool("
                f"total={len(self.hosts_list)}, "
                f"left={len(self.unallocated_addresses)}, "
                f"allocated_addresses={[str(a) for a in self.allocated_addresses]}, "
                f"unallocated_addresses={[str(a) for a in self.unallocated_addresses]}"
                f")"
            )
        except Exception as e:
            raise e
    
    def _sort_spaces(self):
        try:
            self.allocated_addresses.sort()
            self.unallocated_addresses.sort()
        except Exception as e:
            raise e

    def relocate_address(func):
        def wrapper(self, address: ... = None):
            try:
                if address is None:
                    if func.__name__ == 'allocate_address':
                        if not self.unallocated_addresses:
                            raise IndexError("No more unallocated addresses available.")
                        address = self.unallocated_addresses[0]
                    elif func.__name__ == 'unallocate_address':
                        if not self.allocated_addresses:
                            raise IndexError("No more allocated addresses available to unallocate.")
                        address = self.allocated_addresses[-1]
                address = ipaddress.IPv4Address(address)
                src_list = self.allocated_addresses if func.__name__ == 'unallocate_address' else self.unallocated_addresses
                dst_list = self.unallocated_addresses if func.__name__ == 'unallocate_address' else self.allocated_addresses
                if address not in src_list:
                    raise ValueError(f"Error: Address {address} is not {'allocated' if func.__name__ == 'unallocate_address' else 'available'}.")
                src_list.remove(address)
                dst_list.append(address)
                self._sort_spaces()
                return address
            except (ValueError, IndexError) as e:
                raise e

        return wrapper

    @relocate_address
    def allocate_address(self, address=None):
        try:
            if address is None:
                if not self.unallocated_addresses:
                    raise IndexError("No more unallocated addresses available.")
                address = self.unallocated_addresses.pop(0)
                self.allocated_addresses.append(address)
                self._sort_spaces()
                return address
            else:
                return address
        except (IndexError, Exception) as e:
            raise e

    @relocate_address
    def unallocate_address(self, address=None):
        try:
            if address is None:
                if not self.allocated_addresses:
                    raise IndexError("No more allocated addresses available to unallocate.")
                address = self.allocated_addresses.pop(-1)
                self.unallocated_addresses.append(address)
                self._sort_spaces()
                return address
            else:
                return address
        except (IndexError, Exception) as e:
            raise e

