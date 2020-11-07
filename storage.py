from typing import Dict

from petlib.bn import Bn


class StorageServer:

    def __init__(self):
        """
        Server needs a storage for all e_i2 and d_i2 for every user in the system
        Needs a storage
        """
        # Storage of the partial keys corresponding to each client_id
        self._partial_keys: Dict[Bn, (Bn, Bn)] = {}

    def new_user_partial_key(self, client_id: Bn, partial_key: (Bn, Bn)):
        """
        input: user_values is a tuple for this users (e_i2, d_i2). To add to the server proxy storage
        output: success or failure maybe?
        """
        # TODO: Check that client does not yet exist
        self._partial_keys[client_id] = partial_key
    
    def proxy_encryption(self, ciphertext):
        """
        input: ciphertext is a tuple from the user of the ciphertexts and an encrypted set of keywordds
            (c_1, c_2, {c_m1, c_m2, ..., c_m3}). 
        output: none

        Server re-encryptes using {c_2}* = {c_2}^e_i2. It has to do the same for every e_wm. It finally
        stores the tuple (c_1, {c_2)*, {{c_w1*, c_w2*, ..., c_wm*}}}
        """

    def proxy_keyword_search(self, Q):
        """
        input: Q, encrypted hash value of keyword
        output: all ciphertext which contain keyword

        Server computes Q* = Q^{e_j2}. Then it tests all keywords i the encrypted keyword set. if c_{wm}* = Q*,
        then add ciphertext into the result set.
        """
