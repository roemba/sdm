from typing import List
from uuid import uuid4

from models import EncryptedDocument, Keys, CryptoFunctions


"""
Each client of the consultant is represented as a class
"""
class Client:

    def __init__(self):
        #Create unique user identity
        self._id = uuid4()
        self._keys: Keys = None

    @property
    def id(self):
        return self._id

    def assign_keys(self, keys: Keys):
        self._keys = keys

    """
    Input: a document and a list of relevant keywords
    Output: encrypted document and key words
    """
    def encrypt_data(self, plaintext: bytes, search_keywords: List[bytes]) -> EncryptedDocument:
        return CryptoFunctions.encrypt_data(plaintext, search_keywords, self._keys)

    """
    Input: encrypted document
    Returns: decrypted documents using the clients keys
    """
    def data_decrypt(self, encrypted_documents: List[EncryptedDocument]) -> List[bytes]:
        return CryptoFunctions.data_decrypt(encrypted_documents, self._keys)

    """
    Input: keyrword the client wants to search for
    Output: the resulting documents containing the keyword
    """
    def create_trapdoor_q(self, keyword: bytes) -> bytes:
        return CryptoFunctions.create_trapdoor_q(keyword, self._keys)
