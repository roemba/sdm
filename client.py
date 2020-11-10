from hashlib import sha256
from os import urandom
from typing import List, Tuple

from petlib.bn import Bn
from petlib.cipher import Cipher


class Client:

    def __init__(self, id: Bn):
        """
        Should call user key setup to create a key pair of the user
        """
        self._id = id
        self._n = None
        self._e = None
        self._d = None
        self._iv = None

    @property
    def id(self):
        return self._id

    def assign_keys(self, public_key: Bn, partial_key: (Bn, Bn)):
        self._n = public_key
        self._e, self._d = partial_key

    def _encrypt_RSA(self, plaintext: bytes) -> Bn:
        #Already converts using big endian, I think it is unnecessary to convert first to number. 
        return Bn.from_binary(plaintext).mod_pow(self._e, self._n)
        #return Bn.from_num(int.from_bytes(plaintext, byteorder='big')).mod_pow(self._e, self._n)

    def _decrypt_RSA(self, ciphertext: Bn) -> bytes:
        return ciphertext.mod_pow(self._d, self._n).binary()

    def set_seed(self, iv):
        self._iv = iv

    def encrypt_data(self, plaintext: bytes, search_keywords: List[bytes]) -> (Bn, Bn, List[Bn]):
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
        aes = Cipher("AES-128-CTR")
        key = urandom(16)
        # Encrypt the data
        enc = aes.enc(key, self._iv)
        c1 = enc.update(plaintext)
        c1 += enc.finalize()
        # TODO: Check that the modulus n is at least 16 bytes long and large enough for the keywords to fit in
        c2 = self._encrypt_RSA(key)
        cw = [self._encrypt_RSA(sha256(kw).digest()) for kw in search_keywords]
        return c1, c2, cw

    def data_decrypt(self, ciphertext_pairs: List[Tuple[bytes, Bn]]) -> List[bytes]:
        """
        input is the ciphertext extracted from the server for every plaintext item 
              after proxy re-decryption c_1, c_2'
        output: plaintexts which match a search string

        User computs (c_2')^d_i1 ) = (K_x)^{ed} = K_x. Using K_x the user can decrypt the document
        plaintext = {E_{k_x}}^-1(c_1) (because encryption is symmetric so it needs to have an inverse function)
        """
        documents = []
        aes = Cipher("AES-128-CTR")
        for ciphertext_pair in ciphertext_pairs:
            c1, c2_marked = ciphertext_pair
            c2 = self._decrypt_RSA(c2_marked)
            decryption = aes.dec(c2, self._iv)
            plaintext = decryption.update(c1)
            plaintext += decryption.finalize()
            documents.append(plaintext)
        return documents

    def create_trapdoor_q(self, keyword: bytes):
        """
        input: keyword the user wants to search for
        output: Trapdoor for the server to find encrypted documents which contain the keyword

        User computes the hash of the keyword sigma = H(W) an encrypts Q = sigma^{e_j2}. User sends Q to server
        """
        return self._encrypt_RSA(sha256(keyword).digest())
