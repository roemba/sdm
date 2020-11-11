from hashlib import sha256
from typing import Dict, List
from uuid import UUID
from models import Keys, EncryptedDocument, AES
from os import urandom
from hmac import digest as hmac_digest

from petlib.bn import Bn

class Consultant:
    """
    This is the trusted party (consultant) in the protocol, setting up and managing all the keys.
    """

    def __init__(self):
        self._client_keys: Dict[UUID, bytes] = {}

    def generate_client_keys(self, client) -> (Keys, UUID):
        client_keys = Keys()
        
        if client.id in self._client_keys:
            raise ValueError("Cannot generate a new keypair for an already existing client!")

        self._client_keys[client.id] = client_keys

        return client_keys

    def encrypt_data(self, plaintext: bytes, search_keywords: List[bytes], client_id: UUID) -> EncryptedDocument:
        ciphertext, iv = AES.encrypt(plaintext, self._client_keys[client_id].encryption_key)
        encrypted_keywords = [self.create_trapdoor_q(kw) for kw in search_keywords]

        return EncryptedDocument(ciphertext, encrypted_keywords, iv)

    def data_decrypt(self, encrypted_documents: List[EncryptedDocument], client_id: UUID) -> List[bytes]:
        documents = []
        for encrypted_document in encrypted_documents:
            plaintext = AES.decrypt(encrypted_document.ciphertext, self._client_keys[client_id].encryption_key, encrypted_document.iv)
            documents.append(plaintext)

        return documents

    def create_trapdoor_q(self, keyword: bytes, client_id: UUID):
        return hmac_digest(self._client_keys[client_id].hashing_key, keyword, sha256)