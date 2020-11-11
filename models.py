from math import gcd
from typing import List
from os import urandom
from uuid import uuid4, UUID

from petlib.bn import Bn
from petlib.cipher import Cipher

class AES:
    cipher_type = "AES-128-CTR"

    @classmethod
    def encrypt(cls, plaintext: bytes) -> (bytes, bytes, bytes):
        iv = urandom(16)
        key = urandom(16)

        enc = Cipher(cls.cipher_type).enc(key, iv)
        ciphertext = enc.update(plaintext)
        ciphertext += enc.finalize()

        return ciphertext, key, iv

    @classmethod
    def decrypt(cls, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        decryption = Cipher(cls.cipher_type).dec(key, iv)
        plaintext = decryption.update(ciphertext)
        plaintext += decryption.finalize()

        return plaintext

class KeyPair:
    def __init__(self, phi_n: Bn, n: Bn, client_id: int):
        # Generate random e, requirements: 0 < e < phi_n, e and phi_n are coprime and e should be large
        while True:
            random_e = phi_n.random()

            if random_e >= 100 and gcd(random_e, phi_n) == 1:
                break


        self._e = random_e
        self._d = self._e.mod_inverse(phi_n)

        self._client_id = client_id
        self._n = n

    def encrypt_RSA(self, plaintext: bytes) -> Bn:
        return Bn.from_binary(plaintext).mod_pow(self._e, self._n)

    def decrypt_RSA(self, ciphertext: Bn) -> bytes:
        return ciphertext.mod_pow(self._d, self._n).binary()

class EncryptedDocument:

    def __init__(self, ciphertext: Bn, encrypted_key: Bn, encrypted_keywords: List[Bn], iv: bytes):
        self.ciphertext = ciphertext
        self.encrypted_key = encrypted_key
        self.encrypted_keywords = frozenset(encrypted_keywords)
        self.iv = iv