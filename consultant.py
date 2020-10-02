from typing import List

from certificates import Certificate
from member import Member


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
