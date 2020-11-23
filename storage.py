import sys
from typing import Dict, List, Tuple
from uuid import UUID

from models import EncryptedDocument

"""
Server which stores and is able to search in encrypted data
"""
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

    """
    Input: document and user id
    Uploads document into storage based on user id
    """
    def upload_document(self, document: EncryptedDocument, client_id: UUID):
        if client_id not in self._storage:
            self._storage[client_id] = []

        self._storage[client_id].append(document)

    """
    Input: encrypted document title and user id
    Output: Client document with corresponding title
    """
    def download_document(self, encrypted_title: bytes, client_id: UUID) -> EncryptedDocument:
        for document in self._storage[client_id]:
            if document.encrypted_title == encrypted_title:
                return document

    """
    Input: trapdoor for keyword and client id
    Output: returns all documents which contain keyword
    """
    def keyword_search(self, trapdoor_q: bytes, client_id: UUID) -> List[EncryptedDocument]:
        if client_id not in self._storage:
            return []

        return [document for document in self._storage[client_id] if trapdoor_q in document.encrypted_keywords]

    """
    Input: trapdoor for keyword and client id
    Output: returns all encrypted title of documents which contain keyword
    """
    def keyword_filename_search(self, trapdoor_q: bytes, client_id: UUID) -> List[Tuple[bytes, bytes, bytes]]:
        if client_id not in self._storage:
            return []

        return [(doc.encrypted_title, doc.title_iv, doc.title_tag) for doc in self._storage[client_id]
                if trapdoor_q in doc.encrypted_keywords]

    """
    Same logic of search (using trapdoor and client id) but offers to provide a list of keywords
    """
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
