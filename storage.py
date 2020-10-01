from typing import List

from certificates import Certificate


class StorageServer:
    """
    The StorageServer stores financial records for a consultant and their clients.
    """

    def insert(self, certificate: Certificate, data: str):
        pass

    def search(self, certificate: Certificate, keywords: List[str]):
        pass
