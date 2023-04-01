import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

class X25519:
    @staticmethod
    def genkey() -> str:
        return base64.b64encode(
            X25519PrivateKey.generate().private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption(),
            )
        ).decode()

    @staticmethod
    def pubkey(privkey: str) -> str:
        return base64.b64encode(
            X25519PrivateKey.from_private_bytes(base64.b64decode(privkey.encode()))
            .public_key()
            .public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
        ).decode()

    @staticmethod
    def genpsk() -> str:
        return X25519.genkey()
