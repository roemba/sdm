from typing import Tuple, List

from certificates import Certificate


class StorageServer:
    """
    The StorageServer stores financial records for a consultant and their clients.
    """

    def __init__(self):
        self.public_key = None

        # TODO: The storage should be adapted in such a way that we can easily extract only the relevant encrypted data
        self._storage = None  # Collection of (data, index) tuples

    def upload(self, certificate: Certificate, data: Tuple):
        pass

    def search(self, certificate: Certificate, trapdoor) -> List:
        """
        This is the SrhInd(T_L, [I_R, ]PK_s) method defined in the paper.
        Validates the certificate and searches the index that is relevant to the requester.
        The consultant can search all indexes while the clients can only search their own.
        :param certificate: Certificate
        :param trapdoor: Trapdoor representing the query keywords
        :return: List of encrypted data corresponding to the query keywords
        """
        assert certificate.verify(self.public_key)
        # TODO: Important! Make sure to only search through the items accessible to this client

        results = []

        for data, index in self._storage:
            pass

        return results
