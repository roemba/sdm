from math import gcd
from typing import Dict
from os import urandom

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

    def setup_system(self, k) -> Bn:
        """
        input: k is a security parameter
        output: n
        k is used to generate (p, q, n, totient(n), e, d)
        """
        p = Bn.get_prime(k // 2)
        q = Bn.get_prime(k // 2)

        self._n = p * q
        self._phi_n = (p - 1) * (q - 1)

        # TODO: Maybe e needs to be random
        self._e = Bn.from_num(65537)
        self._d = self._e.mod_inverse(self._phi_n)

        iv  = urandom(16)

        return self._n, iv

    def _split_multiplicatively(self, secret: Bn) -> (Bn, Bn):
        # The first share can be a random coprime to phi_n
        while True:
            # Generate a non-zero number below phi_n
            first_share = (self._phi_n - 1).random() + 1

            if gcd(first_share, self._phi_n) == 1:
                break

        # The final share x must multiply with the first share s to equal the secret
        # s * x = secret => x = secret * s
        final_share = secret.mod_mul(first_share.mod_inverse(self._phi_n), self._phi_n)

        return first_share, final_share

    def generate_user_key(self) -> ((Bn, Bn), (Bn, Bn)):
        """
        input: (n) master key
        output: User key pair (e_i1,, d_i1) for each user. 
                Proxy responding key pair (e_i2, d_i2) for each user
        Each pair needs to satisfy e_i1*e_i2 = e mod totient(n). A more thourough description
        in chapter 3.1 of "Shared and Searchable encrypted Data for Untrused Servers" by
        Changyu Dong, Giovanni Russello and Naranker Dulay. 
        """
        e1, e2 = self._split_multiplicatively(self._e)
        d1, d2 = self._split_multiplicatively(self._d)

        return (e1, d1), (e2, d2)