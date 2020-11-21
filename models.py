import sys
from typing import List
from os import urandom
from hmac import digest as hmac_digest
from hashlib import sha256

from petlib.cipher import Cipher


class AES:
    @staticmethod
    def encrypt(plaintext: bytes, key: bytes) -> (bytes, bytes):
        iv = urandom(16)
        assert len(key) == 32

        ciphertext, auth_tag = Cipher.aes_256_gcm().quick_gcm_enc(key, iv, plaintext)
        return ciphertext, iv, auth_tag

    @staticmethod
    def decrypt(ciphertext: bytes, key: bytes, iv: bytes, auth_tag: bytes) -> bytes:
        return Cipher.aes_256_gcm().quick_gcm_dec(key, iv, ciphertext, auth_tag)


class Keys:
    def __init__(self):
        self.encryption_key = urandom(32)
        self.hashing_key = urandom(32)


class EncryptedDocument:
    def __init__(self, ciphertext: bytes, encrypted_keywords: List[bytes], iv: bytes, auth_tag: bytes):
        self.ciphertext = ciphertext
        self.encrypted_keywords = frozenset(encrypted_keywords)
        self.iv = iv
        self.auth_tag = auth_tag

    def __sizeof__(self):
        return sys.getsizeof(self.ciphertext) +\
               sys.getsizeof(self.encrypted_keywords) +\
               sys.getsizeof(self.iv) +\
               sys.getsizeof(self.auth_tag)


class CryptoFunctions:
    @staticmethod
    def encrypt_data(plaintext: bytes, search_keywords: List[bytes], keys: Keys) -> EncryptedDocument:
        ciphertext, iv, auth_tag = AES.encrypt(plaintext, keys.encryption_key)
        encrypted_keywords = [CryptoFunctions.create_trapdoor_q(kw, keys) for kw in search_keywords]
        return EncryptedDocument(ciphertext, encrypted_keywords, iv, auth_tag)

    @staticmethod
    def data_decrypt(encrypted_documents: List[EncryptedDocument], keys: Keys) -> List[bytes]:
        documents = []
        for encrypted_document in encrypted_documents:
            plaintext = AES.decrypt(encrypted_document.ciphertext, keys.encryption_key, encrypted_document.iv, encrypted_document.auth_tag)
            documents.append(plaintext)

        return documents

    @staticmethod
    def create_trapdoor_q(keyword: bytes, keys: Keys) -> bytes:
        return hmac_digest(keys.hashing_key, keyword, sha256)
