from typing import List
from uuid import uuid4

from models import EncryptedDocument, Keys, CryptoFunctions


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
        return CryptoFunctions.encrypt_data(plaintext, search_keywords, self._keys)

    def data_decrypt(self, encrypted_documents: List[EncryptedDocument]) -> List[bytes]:
        return CryptoFunctions.data_decrypt(encrypted_documents, self._keys)

    def create_trapdoor_q(self, keyword: bytes) -> bytes:
        return CryptoFunctions.create_trapdoor_q(keyword, self._keys)
