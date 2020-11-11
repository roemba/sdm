from math import gcd
from typing import List
from os import urandom
from uuid import uuid4, UUID

from petlib.bn import Bn
from petlib.cipher import Cipher

class AES:
    cipher_type = "AES-128-CTR"

    @classmethod
    def encrypt(cls, plaintext: bytes, key: bytes) -> (bytes, bytes, bytes):
        iv = urandom(16)
        assert len(key) == 16

        enc = Cipher(cls.cipher_type).enc(key, iv)
        ciphertext = enc.update(plaintext)
        ciphertext += enc.finalize()

        return ciphertext, iv

    @classmethod
    def decrypt(cls, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        decryption = Cipher(cls.cipher_type).dec(key, iv)
        plaintext = decryption.update(ciphertext)
        plaintext += decryption.finalize()

        return plaintext

class Keys:

    def __init__(self):
        self.encryption_key = urandom(16)
        self.hashing_key = urandom(16)

class EncryptedDocument:

    def __init__(self, ciphertext: Bn, encrypted_keywords: List[Bn], iv: bytes):
        self.ciphertext = ciphertext
        self.encrypted_keywords = frozenset(encrypted_keywords)
        self.iv = iv