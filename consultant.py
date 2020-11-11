from hashlib import sha256
from typing import Dict, List
from uuid import UUID
from models import KeyPair, EncryptedDocument, AES

from petlib.bn import Bn

class Consultant:
    """
    This is the trusted party (consultant) in the protocol, setting up and managing all the keys.
    """

    def __init__(self):
        self._n = None
        self._phi_n = None

        self._e = None
        self._d = None

        self._client_keypairs: Dict[UUID, KeyPair] = {}

    def setup_system(self, k: int) -> Bn:
        """
        input: k is a security parameter
        output: n
        k is used to generate (p, q, n, totient(n))
        """
        p = Bn.get_prime(k // 2)
        q = Bn.get_prime(k // 2)

        self._n = p * q
        self._phi_n = (p - 1) * (q - 1)

        return self._n

    def generate_user_keypair(self, client) -> (KeyPair, UUID):
        kp = KeyPair(self._phi_n, self._n, client.id)
        
        if client.id in self._client_keypairs:
            raise ValueError("Cannot generate a new keypair for an already existing client!")

        self._client_keypairs[client.id] = kp

        return kp

    def encrypt_data(self, plaintext: bytes, search_keywords: List[bytes], client_id: UUID) -> EncryptedDocument:
        ciphertext, key, iv = AES.encrypt(plaintext)
        encrypted_key = self._client_keypairs[client_id].encrypt_RSA(key)
        encrypted_keywords = [self.create_trapdoor_q(kw) for kw in search_keywords]

        return EncryptedDocument(ciphertext, encrypted_key, encrypted_keywords, iv)

    def data_decrypt(self, encrypted_documents: List[EncryptedDocument], client_id: UUID) -> List[bytes]:
        documents = []
        for encrypted_document in encrypted_documents:
            key = self._client_keypairs[client_id].decrypt_RSA(encrypted_document.encrypted_key)
            plaintext = AES.decrypt(encrypted_document.ciphertext, key, encrypted_document.iv)
            documents.append(plaintext)

        return documents

    def create_trapdoor_q(self, keyword: bytes, client_id: UUID):
        return self._client_keypairs[client_id].encrypt_RSA(sha256(keyword).digest())