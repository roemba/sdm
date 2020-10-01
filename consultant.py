from typing import List

from certificates import Certificate


class Consultant:
    """
    This is the Group Manager (GM), who can access all information.
    """

    def __init__(self):
        self._master_key = None

    def setup_system(self, security_parameter):
        """
        This is the SysSet(tau) method defined in the paper.
        Generates the public and secret key, and updates the consultant's master key
        :param security_parameter: Security parameter tau
        :return: Public key and secret key respectively
        """
        self._master_key = None

        return None, None

    def authenticate_group(self, member_count: int) -> List[Certificate]:
        """
        This is the GrpAut(G, PK_s, MK) method defined in the paper.
        Generates a certificate for each user (in the right order).
        :param member_count: Number of members to authenticate
        :return: List of certificates that each member should keep secret
        """
        return []

    # The methods MemJon (member joins) and MemLev (member leaves) are not essential.
