from petlib.bn import Bn


class TTP:
    """
    This is the trusted third party in the protocol. Setting up and managing all the keys
    """

    def __init__(self):
        self._phi_n = None
        self._d = None

    def setup_key_generator(self, k):
        """
        input: k is a security parameter
        output: n (master key)
        k is used to generate (p, q, n, totient(n), e, d)
        """
        p = Bn.get_prime(k)
        q = Bn.get_prime(k)

        # TODO: We might be able to use Carmichael's totient function here instead
        n = p * q
        self._phi_n = (p - 1) * (q - 1)

        e = Bn.from_num(65537)
        self._d = e.mod_inverse(self._phi_n)

        public_key = (e, n)

    def user_key_generator(self):
        """
        input: (n) master key
        output: User key pair (e_i1,, d_i1) for each user. 
                Proxy responding key pair (e_i2, d_i2) for each user
        Each pair needs to satisfy e_i1*e_i2 = e mod totient(n). A more thourough description
        in chapter 3.1 of "Shared and Searchable encrypted Data for Untrused Servers" by
        Changyu Dong, Giovanni Russello and Naranker Dulay. 
        """


    def define_hash(self):
        """
        For this to work all users have to use the same hash function
        """
