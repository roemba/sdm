from typing import List

from certificates import Certificate
from member import Member

from bplib import bp
from petlib.bn import Bn
from copy import copy
from hashlib import sha512

class Consultant(Member):
    """
    This is the Group Manager (GM), who can access all information.
    """

    def __init__(self):
        super().__init__()
        self._master_key = None

    def setup_system(self, security_parameter):
        """
        This is the SysSet(tau) method defined in the paper.
        Generates the master, public and secret key, and updates the consultant's keys
        :param security_parameter: Security parameter tau
        :return: Public key and secret key respectively
        """
        # Step 1
        BG = bp.BpGroup()
        g = BG.gen1()

        q = BG.order()

        rand_values = []
        while len(rand_values) != 3:
            r = q.random()
            if r > 1:
                rand_values.append(r)

        alpha, x, y = rand_values

        X = g * x
        Y = g * y

        # Step 2
        H = lambda value_to_hash: Bn.from_binary(sha512(value_to_hash).digest()).mod(q)
        # TODO

        # Step 3
        P = q.random() * g
        Q = q.random() * q

        rand_values = []
        while len(rand_values) != 2:
            r = q.random()
            if r > 1:
                rand_values.append(r)

        lambda_, sigma = rand_values

        P_dash = P * lambda_
        Q_dash = Q * (lambda_ - sigma)

        # Step 4
        self._public_key = None
        self._secret_key = None
        self._master_key = None

        return None, None

    # TODO: Either in the setup_system or authenticate_group methods the consultant should also generate a certificate
    #  for themselves, perhaps with the convention that the consultant always has ID = 0.

    def authenticate_group(self, member_count: int) -> List[Certificate]:
        """
        This is the GrpAut(G, PK_s, MK) method defined in the paper.
        Generates a certificate for each user (in the right order).
        :param member_count: Number of members to authenticate
        :return: List of certificates that each member should keep secret
        """
        return []

    def request_decryption_keys(self, certificate: Certificate, auxiliary_information: List) -> List:
        """
        This is the GDcKey(U', CT_i[, PK_s, SK_g, MK]) method defined in the paper.
        The consultant verifies the certificates and returns a decryption key for the corresponding encrypted data.
        :param certificate: Certificate
        :param auxiliary_information: Auxiliary information (U') to compute the key
        :return: Decryption keys for the corresponding encrypted data
        """
        assert certificate.verify(self._public_key)

        return []

    # The methods MemJon (member joins) and MemLev (member leaves) are not essential.

# Testing
c = Consultant()
c.setup_system(5)