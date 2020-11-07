from typing import List

from client import Client
from consultant import Consultant
from storage import StorageServer


def setup(consultant: Consultant, clients: List[Client], storage_server: StorageServer):
    # Setup the system for the consultant and storage_server
    public_key = consultant.setup_system(128)
    storage_server.public_key = public_key

    # Setup the system for the clients
    for client in clients:
        # Add client
        client_pair, storage_pair = consultant.generate_user_key()
        client.assign_partial_key(client_pair)
        storage_server.new_user_partial_key(client.id, storage_pair)


# def search_storage_server(consultant: Consultant, member: Member, storage_server: StorageServer, keywords: List[str])\
#         -> List[str]:
#     # Request search from the server
#     trapdoor = member.make_trapdoor(keywords)
#     encrypted_results = storage_server.search(member.certificate, trapdoor)
#
#     # Request decryption keys from the consultant
#     auxiliaries, one_time_keys = member.prepare_decryption_request(len(encrypted_results))
#     decryption_keys = consultant.request_decryption_keys(member.certificate, auxiliaries)
#
#     # Decrypt search results
#     return member.decrypt_data(encrypted_results, decryption_keys, one_time_keys)


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


# def upload_storage_server(member: Member, storage_server: StorageServer, raw_data: str):
#     storage_server.upload(member.certificate, member.build_data(raw_data))
