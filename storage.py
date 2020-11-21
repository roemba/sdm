import sys
from typing import Dict, List
from uuid import UUID

from models import EncryptedDocument


class StorageServer:

    def __init__(self):
        # Storage of encrypted documents, it is a collection of encrypted documents
        self._storage: Dict[UUID, List[EncryptedDocument]] = {}

    def __sizeof__(self):
        size = sys.getsizeof(self._storage)

        for items in self._storage.values():
            for item in items:
                size += sys.getsizeof(item)

        return size

    def upload_document(self, document: EncryptedDocument, client_id: UUID):
        if client_id not in self._storage:
            self._storage[client_id] = []

        self._storage[client_id].append(document)

    def keyword_search(self, trapdoor_q: bytes, client_id: UUID):
        return [document for document in self._storage[client_id] if trapdoor_q in document.encrypted_keywords]
