from hashlib import sha256
from typing import List, Tuple
from uuid import uuid4

from petlib.ec import EcGroup, EcPt

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

    def exchange_keys(self, A1: EcPt, A2: EcPt) -> Tuple[EcPt, EcPt]:
        curve = EcGroup(713)
        g = curve.generator()

        b1 = curve.order().random()
        B1 = g.pt_mul(b1)

        b2 = curve.order().random()
        B2 = g.pt_mul(b2)

        self._keys = Keys()
        self._keys.encryption_key = sha256(A1.pt_mul(b1).export()).digest()
        self._keys.hashing_key = sha256(A2.pt_mul(b2).export()).digest()

        return B1, B2

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
