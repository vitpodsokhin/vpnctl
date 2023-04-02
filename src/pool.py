import ipaddress

class Pool(ipaddress.IPv4Network):
    '''The Pool is a low-level class for the address space allocation functionality.'''
    def __init__(self, address_space: str, hosts_num: int = 0, *args, **kwargs):
        #TODO implement memory friendly mechanism for address allocation
        # for cases when bitmask of the network is less than 24
        # refactor unallocated_addresses from list to generator
        try:
            super().__init__(address_space, *args, **kwargs)
            if hosts_num == 0:
                self.unallocated_addresses = list(self.hosts())
                self.allocated_addresses = []
            elif hosts_num <= self.num_addresses:
                self.allocated_addresses = list(self.hosts())[:hosts_num]
                self.unallocated_addresses = list(self.hosts())[hosts_num:]
            else:
                raise ValueError(
                    f"Error: The number of requested hosts ({hosts_num}) exceeds "
                    f"the number of available hosts in the address space ({self.num_addresses})."
                )
        except ValueError as e:
            raise e

    def __repr__(self) -> str:
        #TODO See implement memory friendly mechanism for address allocation
        try:
            return (
                f"Pool("
                f"total={self.num_addresses-2}, left={len(self.unallocated_addresses)}, "
                f"allocated_addresses={[str(a) for a in self.allocated_addresses]}"
                # f"unallocated_addresses={[str(a) for a in self.unallocated_addresses]}"
                f")"
            )
        except Exception as e:
            raise e
    
    def _sort_spaces(self):
        #TODO See implement memory friendly mechanism for address allocation
        try:
            self.allocated_addresses.sort()
            self.unallocated_addresses.sort()
        except Exception as e:
            raise e

    def relocate_address(func):
        #TODO See implement memory friendly mechanism for address allocation
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
                    raise ValueError(
                        f"Error: Address {address} is not "
                        f"{'allocated' if func.__name__ == 'unallocate_address' else 'available'}."
                    )
                src_list.remove(address)
                dst_list.append(address)
                self._sort_spaces()
                return address
            except (ValueError, IndexError) as e:
                raise e

        return wrapper

    @relocate_address
    def allocate_address(self, address=None):
        #TODO See implement memory friendly mechanism for address allocation
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
        #TODO See implement memory friendly mechanism for address allocation
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

