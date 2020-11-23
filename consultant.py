from hashlib import sha256
from typing import Dict, List
from uuid import UUID

from petlib.bn import Bn
from petlib.ec import EcGroup

from client import Client
from models import Keys, EncryptedDocument, CryptoFunctions

"""
This is the trusted party (consultant) in the protocol, setting up and managing all the keys.
"""
class Consultant:
    def __init__(self):
        self._client_keys: Dict[UUID, Keys] = {}

    """
    For each client, generate a key pair
    """
    def generate_client_keys(self, client: Client) -> (Keys, UUID):
        client_keys = Keys()
        
        if client.id in self._client_keys:
            raise ValueError("Cannot generate a new keypair for an already existing client!")

        self._client_keys[client.id] = client_keys

        return client_keys

    """
    Generate a key pair collaboratively using Elliptic Curve Diffie-Helman Key Exchange
    """
    def exchange_client_keys(self, client: Client):
        curve = EcGroup(713)
        g = curve.generator()

        a1 = curve.order().random()
        A1 = g.pt_mul(a1)

        a2 = curve.order().random()
        A2 = g.pt_mul(a2)

        B1, B2 = client.exchange_keys(A1, A2)

        self._client_keys[client.id] = Keys()
        self._client_keys[client.id].encryption_key = sha256(B1.pt_mul(a1).export()).digest()
        self._client_keys[client.id].hashing_key = sha256(B2.pt_mul(a2).export()).digest()

    """
    Functions necessary to enable the consultant to search the documents
    """
    def encrypt_data(self, plaintext: bytes, search_keywords: List[bytes], client_id: UUID) -> EncryptedDocument:
        return CryptoFunctions.encrypt_data(plaintext, search_keywords, self._client_keys[client_id])

    def data_decrypt(self, encrypted_documents: List[EncryptedDocument], client_id: UUID) -> List[bytes]:
        return CryptoFunctions.data_decrypt(encrypted_documents, self._client_keys[client_id])

    def create_trapdoor_q(self, keyword: bytes, client_id: UUID):
        return CryptoFunctions.create_trapdoor_q(keyword, self._client_keys[client_id])
