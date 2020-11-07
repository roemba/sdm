

class Certificate:
    """
    Certificates are used to verify that a person has access.
    """

    def verify(self, public_key) -> bool:
        """
        This is the MemChk(CT_i, PK_s) method defined in the paper.
        Verifies that a certificate is well-formed, returns True if it is.
        :param public_key: Public properties
        :return: True when the certificate is well-formed, False if not.
        """
        pass
