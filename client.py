from hashlib import sha256
from os import urandom
from typing import List, Tuple

from petlib.bn import Bn

from uuid import UUID, uuid4
from models import KeyPair, EncryptedDocument, AES


class Client:

    def __init__(self):
        """
        Should call user key setup to create a key pair of the user
        """
        self._id = uuid4()
        self._keypair = None
        self._iv = None

    @property
    def id(self):
        return self._id

    def assign_keypair(self, keypair: KeyPair):
        self._keypair = keypair

    def encrypt_data(self, plaintext: bytes, search_keywords: List[bytes]) -> EncryptedDocument:
        """
        input: plaintext to be encrypted and a set of searching keyword for that document
        output: success maybe?
        
        The  encryption is done using a symmetric encryption algorithm  E.
        The user chooses a key K_x (for each plaintext) uniformally randomly 
        from the key space ef E to encrypt the plaintext.
        c_1 = E_{k_x}(plaintext_x) - plaintext encrypted under k_x using E
        c_2 = (K_x)^e_i1 - key chosen encrypted under RSA

        The user computes a hash value for each search keyword w_m and sigma_wm = H(W_m)
        c_wm = (sigma_wm)^e_i1 hash encrypted under RSA encryption and sends to the server
        """
        # Select a one-time random key and IV for AES-128-CTR
        ciphertext, key, iv = AES.encrypt(plaintext)
        # TODO: Check that the modulus n is at least 16 bytes long and large enough for the keywords to fit in
        encrypted_key = self._keypair.encrypt_RSA(key)
        encrypted_keywords = [self.create_trapdoor_q(kw) for kw in search_keywords]
        return EncryptedDocument(ciphertext, encrypted_key, encrypted_keywords, iv)

    def data_decrypt(self, encrypted_documents: List[EncryptedDocument]) -> List[bytes]:
        """
        input is the ciphertext extracted from the server for every plaintext item 
              after proxy re-decryption c_1, c_2'
        output: plaintexts which match a search string

        User computs (c_2')^d_i1 ) = (K_x)^{ed} = K_x. Using K_x the user can decrypt the document
        plaintext = {E_{k_x}}^-1(c_1) (because encryption is symmetric so it needs to have an inverse function)
        """
        documents = []
        for encrypted_document in encrypted_documents:
            key = self._keypair.decrypt_RSA(encrypted_document.encrypted_key)
            plaintext = AES.decrypt(encrypted_document.ciphertext, key, encrypted_document.iv)
            documents.append(plaintext)

        return documents

    def create_trapdoor_q(self, keyword: bytes):
        """
        input: keyword the user wants to search for
        output: Trapdoor for the server to find encrypted documents which contain the keyword

        User computes the hash of the keyword sigma = H(W) an encrypts Q = sigma^{e_j2}. User sends Q to server
        """
        return self._keypair.encrypt_RSA(sha256(keyword).digest())
