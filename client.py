from hashlib import sha256
from os import urandom
from typing import List, Tuple

from petlib.bn import Bn

from uuid import UUID, uuid4
from models import EncryptedDocument, AES, Keys
from hmac import digest as hmac_digest


class Client:

    def __init__(self):
        """
        Should call user key setup to create a key pair of the user
        """
        self._id = uuid4()
        self._keys = None
        self._iv = None

    @property
    def id(self):
        return self._id

    def assign_keys(self, keys: Keys):
        self._keys = keys

    def encrypt_data(self, plaintext: bytes, search_keywords: List[bytes]) -> EncryptedDocument:
        ciphertext, iv = AES.encrypt(plaintext, self._keys.encryption_key)
        encrypted_keywords = [self.create_trapdoor_q(kw) for kw in search_keywords]
        return EncryptedDocument(ciphertext, encrypted_keywords, iv)

    def data_decrypt(self, encrypted_documents: List[EncryptedDocument]) -> List[bytes]:
        documents = []
        for encrypted_document in encrypted_documents:
            plaintext = AES.decrypt(encrypted_document.ciphertext, self._keys.encryption_key, encrypted_document.iv)
            documents.append(plaintext)

        return documents

    def create_trapdoor_q(self, keyword: bytes):
        return hmac_digest(self._keys.hashing_key, keyword, sha256)
