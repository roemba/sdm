from typing import Dict, List, Tuple

from petlib.bn import Bn


class EncryptedDocument:

    def __init__(self, keywords: List[Bn], ciphertext_pair: Tuple[bytes, Bn]):
        self._keywords = set(keywords)
        self._ciphertext_pair = ciphertext_pair

    def __contains__(self, keyword: Bn):
        """
        Checks whether a keyword occurs in this EncryptedDocument.

        :param keyword: Keyword to search for (trapdoor)
        :return: True when the keyword is contained in this EncryptedDocument
        """
        return keyword in self._keywords

    @property
    def ciphertext_pair(self):
        return self._ciphertext_pair


class StorageServer:

    def __init__(self):
        """
        Server needs a storage for all e_i2 and d_i2 for every user in the system
        Needs a storage
        """
        # Storage of the partial keys corresponding to each client_id
        self._partial_keys: Dict[Bn, (Bn, Bn)] = {}
        self._n = None
        self.public_key = None
        # Storage of encrypted documents, it is a collection of encrypted documents
        self._storage: List[EncryptedDocument] = []

    def _encrypt_RSA(self, current_e, encryption_text: Bn) -> Bn:
        return encryption_text.mod_pow(current_e, self.public_key)

    def _decrypt_RSA(self, current_d, ciphertext: Bn) -> Bn:
        return ciphertext.mod_pow(current_d, self.public_key)

    def new_user_partial_key(self, client_id: Bn, partial_key: Tuple[Bn, Bn]):
        """
        input: user_values is a tuple for this users (e_i2, d_i2). To add to the server proxy storage
        output: success or failure maybe?
        """
        # TODO: Check that client does not yet exist
        self._partial_keys[client_id] = partial_key
    
    def proxy_encryption(self, client_id, c1, c2, cw):
        """
        input: ciphertext is a tuple from the user of the ciphertexts and an encrypted set of keywordds
            (c_1, c_2, {c_m1, c_m2, ..., c_m3}). 
        output: none

        Server re-encryptes using {c_2}* = {c_2}^e_i2. It has to do the same for every e_wm. It finally
        stores the tuple (c_1, {c_2)*, {{c_w1*, c_w2*, ..., c_wm*}}}
        """
        client_e, client_d = self._partial_keys[client_id]
        c2_starred = self._encrypt_RSA(c2, client_e)
        cw_starred = [self._encrypt_RSA(cwm, client_e) for cwm in cw]
        #TODO we need a storing method for the ciphertext below
        ciphertext =  (c1, c2_starred, cw_starred)

    def proxy_decryption(self, client_id, ciphertext_pairs: List[Tuple[bytes, Bn]]) -> List[Tuple[bytes, Bn]]:
        """
        input: id of current client, all ciphertext pairs (c1, c2*) which matched a keyword
        output: ciphertext pair (c1, c2') where c2' = (c2*)^d_i2 for user i

        a list of ciphertexts which match a keyword
        """
        if len(ciphertext_pairs) == 0:
            raise ValueError("No matches for keyword were found")
        client_e, client_d = self._partial_keys[client_id]
        ciphertext_pairs_marked = []
        for ciphertext_pair in ciphertext_pairs:
            c2_marked = self._decrypt_RSA(client_d, ciphertext_pair[1])
            ciphertext_pairs_marked.append((ciphertext_pair[0], c2_marked)) ## Fixed, shouldn't  be pair
        return ciphertext_pairs_marked

    def upload_encrypted_document(self, client_id: Bn, ciphertexts: Tuple[bytes, Bn, List[Bn]]):
        client_e, client_d = self._partial_keys[client_id]
        c1, c2, cws = ciphertexts
        c2_star = self._encrypt_RSA(client_e, c2)
        cws_star = [self._encrypt_RSA(client_e, cw) for cw in cws]
        self._storage.append(EncryptedDocument(cws_star, (c1, c2_star)))

    def proxy_keyword_search(self, client_id: Bn, trapdoor_q: Bn):
        """
        input: Q, encrypted hash value of keyword
        output: all ciphertext pairs (c1, c2') which contain keyword

        Server computes Q* = Q^{e_j2}. Then it tests all keywords i the encrypted keyword set. if c_{wm}* = Q*,
        then add ciphertext into the result set.
        """
        client_e, client_d = self._partial_keys[client_id]
        q_starred = self._encrypt_RSA(client_e, trapdoor_q)
        print('q_starred: ', q_starred)
        results = [document.ciphertext_pair for document in self._storage if q_starred in document]
        print('proxy keyword search: ', results)
        return self.proxy_decryption(client_id, results)
