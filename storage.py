from typing import List

from certificates import Certificate


# TODO: Move this functionality to a Member class, as well as DatAux and MemDct
class Query:

    def __init__(self, keywords: List[str], public_key, secret_Key):
        """
        This is the MakTrp(L', PK_s, SK_g) method defined in the paper.
        Creates a Trapdoor of the keyword list that represents a query.
        :param keywords: Keyword list
        :param public_key: Public key
        :param secret_Key: Secret key of the requester
        """
        pass


class StorageServer:
    """
    The StorageServer stores financial records for a consultant and their clients.
    """

    def __init__(self):
        self._public_key = None

    def insert(self, certificate: Certificate, data: str):
        pass

    def search(self, certificate: Certificate, query: Query):
        """
        This is the SrhInd(T_L, I_R, PK_s) method defined in the paper.
        Validates the certificate and searches the index that is relevant to the requester.
        The consultant can search all indexes while the clients can only search their own.
        :param certificate: Certificate
        :param query: Trapdoor representing the query
        :return: List of encrypted data corresponding to the query
        """
        pass
