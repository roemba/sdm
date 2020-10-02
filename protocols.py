from typing import List

from consultant import Consultant
from member import Member
from storage import StorageServer

# TODO: Write docstrings


def setup(consultant: Consultant, members: List[Member], storage_server: StorageServer):
    # Setup the system for the consultant and storage_server
    public_key, secret_key = consultant.setup_system(128)
    storage_server.public_key = public_key

    # Setup the system for the clients
    for member, certificate in zip(members, consultant.authenticate_group(len(members))):
        member.certificate = certificate
        member.assign_keys(public_key, secret_key)


def search_storage_server(consultant: Consultant, member: Member, storage_server: StorageServer, keywords: List[str])\
        -> List[str]:
    # Request search from the server
    trapdoor = member.make_trapdoor(keywords)
    encrypted_results = storage_server.search(member.certificate, trapdoor)

    # Request decryption keys from the consultant
    auxiliaries, one_time_keys = member.prepare_decryption_request(len(encrypted_results))
    decryption_keys = consultant.request_decryption_keys(member.certificate, auxiliaries)

    # Decrypt search results
    return member.decrypt_data(encrypted_results, decryption_keys, one_time_keys)


def search_storage_server_consultant(consultant: Consultant, storage_server: StorageServer, keywords: List[str])\
        -> List[str]:
    # Request search from the server
    trapdoor = consultant.make_trapdoor(keywords)
    encrypted_results = storage_server.search(consultant.certificate, trapdoor)

    # TODO: Modified decryption protocol:
    #  this can maybe be done more simply because the consultant does not have to communicate with themselves.

    return []


def upload_storage_server(member: Member, storage_server: StorageServer, raw_data: str):
    storage_server.upload(member.certificate, member.build_data(raw_data))


# TODO: Consider implementing members_join and members_leave protocols
