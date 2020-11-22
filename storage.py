import sys
from typing import Dict, List, Tuple
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

    def download_document(self, encrypted_title: bytes, client_id: UUID) -> EncryptedDocument:
        for document in self._storage[client_id]:
            if document.encrypted_title == encrypted_title:
                return document

    def keyword_search(self, trapdoor_q: bytes, client_id: UUID) -> List[EncryptedDocument]:
        if client_id not in self._storage:
            return []

        return [document for document in self._storage[client_id] if trapdoor_q in document.encrypted_keywords]

    def keyword_filename_search(self, trapdoor_q: bytes, client_id: UUID) -> List[Tuple[bytes, bytes, bytes]]:
        if client_id not in self._storage:
            return []

        return [(doc.encrypted_title, doc.title_iv, doc.title_tag) for doc in self._storage[client_id]
                if trapdoor_q in doc.encrypted_keywords]

    def conjunctive_keyword_search(self, trapdoors: List[bytes], client_id: UUID) -> List[EncryptedDocument]:
        if client_id not in self._storage:
            return []

        return [document for document in self._storage[client_id]
                if all([trapdoor in document.encrypted_keywords for trapdoor in trapdoors])]

    def conjunctive_keyword_filename_search(self, trapdoors: List[bytes], client_id: UUID) -> List[Tuple[bytes, bytes, bytes]]:
        if client_id not in self._storage:
            return []

        return [(doc.encrypted_title, doc.title_iv, doc.title_tag) for doc in self._storage[client_id]
                if all([trapdoor in doc.encrypted_keywords for trapdoor in trapdoors])]
