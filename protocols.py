from typing import List

from consultant import Consultant
from member import Member
from storage import StorageServer


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
