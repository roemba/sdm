class TTP():
    """
    This is the trusted third party in the protocol. Setting up and managing all the keys
    """

    def __init__(self):
        self.master_key = None

    def setup_key_generator(self, k):
        """
        input: k is a security parameter
        output: n (master key)
        k is used to generate (p, q, n, totient(n), e, d)
        """

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