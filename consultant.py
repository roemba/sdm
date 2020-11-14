from typing import Dict, List
from uuid import UUID

from models import Keys, EncryptedDocument, CryptoFunctions


class Consultant:
    """
    This is the trusted party (consultant) in the protocol, setting up and managing all the keys.
    """

    def __init__(self):
        self._client_keys: Dict[UUID, Keys] = {}

    def generate_client_keys(self, client) -> (Keys, UUID):
        client_keys = Keys()
        
        if client.id in self._client_keys:
            raise ValueError("Cannot generate a new keypair for an already existing client!")

        self._client_keys[client.id] = client_keys

        return client_keys

    def encrypt_data(self, plaintext: bytes, search_keywords: List[bytes], client_id: UUID) -> EncryptedDocument:
        return CryptoFunctions.encrypt_data(plaintext, search_keywords, self._client_keys[client_id])

    def data_decrypt(self, encrypted_documents: List[EncryptedDocument], client_id: UUID) -> List[bytes]:
        return CryptoFunctions.data_decrypt(encrypted_documents, self._client_keys[client_id])

    def create_trapdoor_q(self, keyword: bytes, client_id: UUID):
        return CryptoFunctions.create_trapdoor_q(keyword, self._client_keys[client_id])