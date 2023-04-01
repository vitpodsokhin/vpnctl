#!/usr/bin/env python3

import unittest
import ipaddress
from vpn import VPN

class TestVPN(unittest.TestCase):

    def setUp(self):
        self.vpn = VPN(ipaddress.IPv4Network("10.0.0.0/29"))

    def test_add_peer(self):
        peer = self.vpn.add_peer()
        self.assertEqual(len(self.vpn.peers), 1)
        self.assertEqual(peer['address'], "10.0.0.1")
        self.assertFalse(peer['connected'])

if __name__ == '__main__':
    unittest.main()


    
    # def test_remove_peer(self):
    #     peer = self.vpn.add_peer()
    #     self.assertTrue(self.vpn.remove_peer(peer['address']))
    #     self.assertEqual(len(self.vpn.peers), 0)
    #     with self.assertRaises(ValueError):
    #         self.vpn.remove_peer("10.0.0.100")

    # def test_connect_peer(self):
    #     peer = self.vpn.add_peer()
    #     self.assertTrue(self.vpn.connect_peer(peer['address']))
    #     self.assertTrue(peer['connected'])
    #     with self.assertRaises(ValueError):
    #         self.vpn.connect_peer(peer['address'])

    # def test_disconnect_peer(self):
    #     peer = self.vpn.add_peer()
    #     self.vpn.connect_peer(peer['address'])
    #     self.assertTrue(self.vpn.disconnect_peer(peer['address']))
    #     self.assertFalse(peer['connected'])
    #     with self.assertRaises(ValueError):
    #         self.vpn.disconnect_peer(peer['address'])

    # def test_add_peer_fail(self):
    #     for i in range(256):
    #         self.vpn.add_peer()
    #     with self.assertRaises(ValueError):
    #         self.vpn.add_peer()
