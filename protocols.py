from typing import List

from petlib.bn import Bn

from client import Client
from consultant import Consultant
from storage import StorageServer


def setup(consultant: Consultant, clients: List[Client], storage_server: StorageServer):
    # Setup the system for the consultant and storage_server
    public_key, iv = consultant.setup_system(128)
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
    print('search results: ', results)
    return [byte_result.decode(encoding="ISO-8859-1") for byte_result in client.data_decrypt(encrypted_results)]


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
    #docs = ["Hi my name is Jelle yo"]
    my_clients = [Client(Bn.from_num(1))]
    my_server = StorageServer()
    my_consultant = Consultant()
    setup(my_consultant, my_clients, my_server)

    # TODO: Jelle to Vasanth
    # So the code here just sets up one client, one storage server and one consultant and I am trying to
    # upload a document and then to decrypt it with the same client. Right now this code is *super* messy as I just
    # wanted to check if it was working (and it doesn't seem to work). Could you have a look if you can get this
    # working? If it gets too frustrating we can discuss with the group haha.
    # Right now searching also does not seem to be working. I was trying to find documents containing "my" but it
    # does not manage to find any results (or so it seems).
    for doc in docs:
        upload_storage_server(my_clients[0], my_server, doc)
    # has to now be decrypted by proxy server and then the user
    decrypt_proxy = my_server.proxy_decryption(my_clients[0].id, [my_server._storage[0].ciphertext_pair])
    decrypt_user = my_clients[0].data_decrypt(decrypt_proxy)
    for i, v in enumerate(docs):
        print(f'doc{i}:', my_server._storage[i]._ciphertext_pair, my_server._storage[i]._keywords)


    # A user is able to add and decrypt their own document. Searching is fine when there is only document returned
    # but when there are multiple docs being returned, it leads to nonsensical decryptions when printing the results
    # even though the keyword matches correctly. encoding method had to be changed to "ISO-8859-1" for the results to
    # be returned otherwise it fails
    #
    # searching for Hello should return two documents correctly decrypted but only the first one seems fine.
    # re-run the file if you get any errors - i get multiple outputs
    print(decrypt_user[0].decode('utf-8'))
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