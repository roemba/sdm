from typing import List

from petlib.bn import Bn
from petlib.cipher import Cipher

from client import Client
from consultant import Consultant
from storage import StorageServer


def setup(consultant: Consultant, clients: List[Client], storage_server: StorageServer):
    # Setup the system for the clients
    for client in clients:
        # Add client
        keypair = consultant.generate_user_keypair(client)
        client.assign_keypair(keypair)

def upload_storage_server(client: Client, storage_server: StorageServer, document: str):
    # Encrypt the document
    keywords = document.split()
    encrypted_document = client.encrypt_data(document.encode(), [keyword.encode() for keyword in keywords])

    # Upload to the storage server
    storage_server.upload_document(encrypted_document, client.id)


if __name__ == '__main__':
    docs = ["Hi my name is Jelle yo", "Hello name Abcd yo", "Hi Jelle yo", "is Hello my yo"]
    doc2 = "Abcd yee"
    my_clients = [Client(), Client()]
    my_server = StorageServer()
    my_consultant = Consultant(256)
    setup(my_consultant, my_clients, my_server)

    for doc in docs:
        upload_storage_server(my_clients[0], my_server, doc)
    upload_storage_server(my_clients[1], my_server, doc2)

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
    except Exception as e:
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