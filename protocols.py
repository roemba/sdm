from typing import List, Iterable, Set, Tuple

from petlib.bn import Bn
from petlib.cipher import Cipher

from client import Client
from consultant import Consultant
from models import AES
from storage import StorageServer

"""
Method testing
"""
def setup(consultant: Consultant, clients: List[Client]):
    # Setup the system for the clients
    for client in clients:
        # Add client
        client_keys = consultant.generate_client_keys(client)
        client.assign_keys(client_keys)


def upload_storage_server(client: Client, storage_server: StorageServer, document: str, keywords: List[str]):
    upload_storage_server_bytes(client, storage_server, document.encode(), [keyword.encode() for keyword in keywords])


def upload_storage_server_bytes(client: Client, storage_server: StorageServer, document: bytes, keywords: List[bytes]):
    # Encrypt the document
    encrypted_document = client.encrypt_data(document, keywords)

    # Upload to the storage server
    storage_server.upload_document(encrypted_document, client.id)


def upload_storage_server_filename(client: Client, storage_server: StorageServer, title: str, document: str, keywords: Set[str]):
    # Encrypt the document
    enc = client.encrypt_data(document.encode(), [keyword.encode() for keyword in keywords])
    enc.encrypted_title, enc.title_iv, enc.title_tag = AES.encrypt(title.encode(), client._keys.encryption_key)

    # Upload to the storage server
    storage_server.upload_document(enc, client.id)


def search_storage_server_filenames(client: Client, storage_server: StorageServer, keywords: Set[str]) -> List[Tuple[str, bytes]]:
    trapdoors = [client.create_trapdoor_q(kw.encode()) for kw in keywords]
    encrypted_titles = storage_server.conjunctive_keyword_filename_search(trapdoors, client.id)

    results = []
    for encrypted_title, iv, tag in encrypted_titles:
        title = AES.decrypt(encrypted_title, client._keys.encryption_key, iv, tag).decode()
        results.append((title, encrypted_title))

    return results


def tests():
    docs = ["Hi my name is Jelle yo", "Hello name Abcd yo", "Hi Jelle yo", "is Hello my yo"]
    doc2 = "Abcd yee"
    my_clients = [Client(), Client()]
    my_server = StorageServer()
    my_consultant = Consultant()
    setup(my_consultant, my_clients)

    for doc in docs:
        upload_storage_server(my_clients[0], my_server, doc, doc.split())
    upload_storage_server(my_clients[1], my_server, doc2, doc2.split())

    # Search for a document with 'Hi' in it using Client 1 - should succeed
    hi_trapdoor_1 = my_clients[0].create_trapdoor_q("Hi".encode())
    results_1 = my_server.keyword_search(hi_trapdoor_1, my_clients[0].id)
    decrypted_results_1 = my_clients[0].data_decrypt(results_1)
    assert (docs[0].encode() in decrypted_results_1) and (docs[2].encode() in decrypted_results_1)
    assert len(results_1) == 2

    # Search for a document with 'Hi' in it using Client 2 - should fail
    hi_trapdoor_2 = my_clients[1].create_trapdoor_q("Hi".encode())
    results_2 = my_server.keyword_search(hi_trapdoor_2, my_clients[1].id)
    assert len(results_2) == 0

    # Client 2 should not be able to decrypt client 1's results
    exception_happened = False
    try:
        decrypted_results_2 = my_clients[1].data_decrypt(results_1)
    except Exception:
        exception_happened = True

    assert exception_happened

    # Consultant should be able to decrypt client 1's results
    decrypted_results_3 = my_consultant.data_decrypt(results_1, my_clients[0].id)
    assert (docs[0].encode() in decrypted_results_1) and (docs[2].encode() in decrypted_results_1)
    assert len(results_1) == 2

    # Consultant should be able to search through client 1's results
    hi_trapdoor_3 = my_consultant.create_trapdoor_q("Hi".encode(), my_clients[0].id)
    results_4 = my_server.keyword_search(hi_trapdoor_3, my_clients[0].id)
    assert results_4 == results_1


if __name__ == '__main__':
    tests()
