from typing import List

from petlib.bn import Bn

from client import Client
from consultant import Consultant
from storage import StorageServer


def setup(consultant: Consultant, clients: List[Client], storage_server: StorageServer):
    # Setup the system for the consultant and storage_server
    public_key, iv = consultant.setup_system(256)
    storage_server.public_key = public_key
    # Setup the system for the clients
    for client in clients:
        # Add client
        client_pair, storage_pair = consultant.generate_user_key()
        client.assign_keys(public_key, client_pair)
        client.set_seed(iv)
        storage_server.new_user_partial_key(client.id, storage_pair)


def search_storage_server(client: Client, storage_server: StorageServer, keyword: str) -> List[str]:
    # Request search from the server
    trapdoor = client.create_trapdoor_q(bytes(keyword, encoding='utf-8'))
    encrypted_results = storage_server.proxy_keyword_search(client.id, trapdoor)
    # Decrypt search results (and go from bytes to strings)
    results = [_ for _ in client.data_decrypt(encrypted_results)]
    return [byte_result.decode() for byte_result in client.data_decrypt(encrypted_results)]


# def search_storage_server_consultant(consultant: Consultant, storage_server: StorageServer, keywords: List[str])\
#         -> List[str]:
#     # Request search from the server
#     trapdoor = consultant.make_trapdoor(keywords)
#     encrypted_results = storage_server.search(consultant.certificate, trapdoor)
#
#     # TODO: Modified decryption protocol:
#     #  this can maybe be done more simply because the consultant does not have to communicate with themselves.
#
#     return []


def upload_storage_server(client: Client, storage_server: StorageServer, document: str):
    # Encrypt the document
    keywords = [bytes(keyword, encoding='utf-8') for keyword in document.split()]
    ciphertexts = client.encrypt_data(bytes(document, encoding='utf-8'), keywords)
    # Upload to the storage server
    storage_server.upload_encrypted_document(client.id, ciphertexts)


if __name__ == '__main__':
    docs = ["Hi my name is Jelle yo", "Hello name Abcd yo", "Hi Jelle yo", "is Hello my yo"]
    doc2 = "Abcd yee"
    my_clients = [Client(Bn.from_num(1)), Client(Bn.from_num(2))]
    my_server = StorageServer()
    my_consultant = Consultant()
    setup(my_consultant, my_clients, my_server)

    for doc in docs:
        upload_storage_server(my_clients[0], my_server, doc)
    upload_storage_server(my_clients[1], my_server, doc2)
    decrypt_proxy = my_server.proxy_decryption(my_clients[0].id, [my_server._storage[0].ciphertext_pair])
    decrypt_user = my_clients[0].data_decrypt(decrypt_proxy)



    # to do
    # Generate different e and d for each client
    # Share each client's e with the storage server
    # Remove re-encryption/decryption from storage server
    #

    print(my_clients[0].data_decrypt([my_server.proxy_decryption(my_clients[0].id, [my_server._storage[0].ciphertext_pair])[0]])[0].decode('utf-8'))
    results = search_storage_server(my_clients[0], my_server, "Abcd")
    print(results)
    results = search_storage_server(my_clients[0], my_server, "yo")
    print(results)
    print(search_storage_server(my_clients[0], my_server, "Hi"))
    print(search_storage_server(my_clients[0], my_server, "Hello"))
    print(search_storage_server(my_clients[0], my_server, "is"))
    decrypt_proxy = my_server.proxy_decryption(my_clients[0].id, [my_server._storage[3].ciphertext_pair])
    decrypt_user = my_clients[0].data_decrypt(decrypt_proxy)
    print(decrypt_user[0].decode('utf-8'))
    print(my_clients[1].data_decrypt([my_server.proxy_decryption(my_clients[1].id, [my_server._storage[4].ciphertext_pair])[0]])[
              0].decode('utf-8'))