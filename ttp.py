from math import gcd
from typing import List, Tuple

from petlib.bn import Bn


class TTP:
    """
    This is the trusted third party in the protocol. Setting up and managing all the keys
    """

    def __init__(self):
        self._n = None
        self._phi_n = None

        self._e = None
        self._d = None

    def setup_key_generator(self, k) -> None:
        """
        input: k is a security parameter
        output: n (master key)
        k is used to generate (p, q, n, totient(n), e, d)
        """
        p = Bn.get_prime(k)
        q = Bn.get_prime(k)

        self._n = p * q
        self._phi_n = (p - 1) * (q - 1)

        self._e = Bn.from_num(65537)
        self._d = self._e.mod_inverse(self._phi_n)

    def _split_multiplicatively(self, secret: Bn, share_count: int):
        shares = []
        product = Bn.from_num(1)

        # The first shares can be random coprimes
        for i in range(share_count - 1):
            # Generate a random coprime to phi_n
            while True:
                # Generate a non-zero number below phi_n
                number = (self._phi_n - 1).random() + 1

                if gcd(number, self._phi_n) == 1:
                    break

            shares.append(number)
            product = product.mod_mul(number, self._phi_n)

        # The final share x must make sure the product of all shares equals the secret
        # s_0 * ... * s_{i-1} * x = secret => x = secret * inv(s_0 * ... * s_{i-1})
        final_share = secret.mod_mul(product.mod_inverse(self._phi_n), self._phi_n)
        shares.append(final_share)

        return shares

    def user_key_generator(self, user_count) -> List[Tuple[Bn, Bn]]:
        """
        input: (n) master key
        output: User key pair (e_i1,, d_i1) for each user. 
                Proxy responding key pair (e_i2, d_i2) for each user
        Each pair needs to satisfy e_i1*e_i2 = e mod totient(n). A more thourough description
        in chapter 3.1 of "Shared and Searchable encrypted Data for Untrused Servers" by
        Changyu Dong, Giovanni Russello and Naranker Dulay. 
        """
        e_shares = self._split_multiplicatively(self._e, user_count)
        d_shares = self._split_multiplicatively(self._d, user_count)

        return [(e, d) for e, d in zip(e_shares, d_shares)]

    def define_hash(self):
        """
        For this to work all users have to use the same hash function
        """
