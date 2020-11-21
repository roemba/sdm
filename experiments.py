import os
import sys
import time
import statistics
from itertools import product
from typing import List

from client import Client
from consultant import Consultant
from protocols import setup, upload_storage_server_bytes
from storage import StorageServer


class SystemSetup:

    def __init__(self, number_of_clients: int):
        self._clients = [Client() for _ in range(number_of_clients)]
        self._server = StorageServer()
        self._consultant = Consultant()

    @property
    def clients(self) -> List[Client]:
        return self._clients

    @property
    def consultant(self) -> Consultant:
        return self._consultant


def evaluate_setup_runtime():
    experiment_count = 100
    run_count = 100
    client_counts = [5, 10, 15, 20, 25, 30, 45, 50]
    print(f"Evaluate setup runtime for client counts {client_counts}, performing {experiment_count} experiments of "
          f"{run_count} runs.")

    runtimes = []
    standard_deviations = []

    for client_count in client_counts:
        # Generate test data
        test_data = [[SystemSetup(client_count) for _ in range(run_count)] for _ in range(experiment_count)]

        # Perform runtime analysis
        experiment_runtimes = []

        for experiment_data in test_data:
            start = time.monotonic()

            for run_data in experiment_data:
                setup(run_data.consultant, run_data.clients)

            runtime = (time.monotonic() - start) / run_count * 1000
            experiment_runtimes.append(runtime)

        runtimes.append(statistics.mean(experiment_runtimes))
        standard_deviations.append(statistics.stdev(experiment_runtimes))

    print(f"Runtimes: {runtimes} ms")
    print(f"Standard deviations: {standard_deviations} ms")


def evaluate_upload_runtime():
    experiment_count = 100

    print("Evaluate upload for a single run")

    document_sizes = [16 * 1024, 256 * 1024, 1024 * 1024]  # 16kB, 256kB, 1MB
    keyword_counts = [10, 100, 1000]

    # Generate test data
    client = Client()
    consultant = Consultant()
    server = StorageServer()

    setup(consultant, [client])

    test_documents = [[os.urandom(document_size) for _ in range(experiment_count)] for document_size in document_sizes]
    test_keywords = [[[os.urandom(8) for _ in range(keyword_count)] for _ in range(experiment_count)] for keyword_count in keyword_counts]

    # perform runtime analysis
    for experiment_documents in test_documents:
        print(f"Trying for document sizes: {document_sizes}")
        for experiment_keywords in test_keywords:
            print(f"- Trying for keyword counts: {keyword_counts}")
            start = time.monotonic()

            for document, keywords in zip(experiment_documents, experiment_keywords):
                upload_storage_server_bytes(client, server, document, keywords)
                server._storage = {}

            runtime = (time.monotonic() - start) / experiment_count * 1000
            print(runtime)


def evaluate_search_runtime():
    experiment_count = 100
    run_count = 100

    print("Evaluate 100 searches")

    document_counts = [16, 64, 256]
    keyword_counts = [10, 100, 1000]

    # Generate test data
    client = Client()
    consultant = Consultant()
    server = StorageServer()

    setup(consultant, [client])

    # Perform runtime analysis
    for dc, kc in product(document_counts, keyword_counts):
        encrypted_documents = [[client.encrypt_data(os.urandom(8), [os.urandom(8) for _ in range(kc)]) for _ in range(dc)] for _ in range(experiment_count)]

        start = time.monotonic()
        for experiment_documents in encrypted_documents:
            server._storage[client.id] = experiment_documents

            for _ in range(run_count):
                server.keyword_search(client.create_trapdoor_q(os.urandom(8)), client.id)

        runtime = (time.monotonic() - start) / experiment_count * 1000
        print(f"{dc} documents with {kc} keywords: {runtime} ms")


def evaluate_upload_bandwidth():
    experiment_count = 100

    print("Evaluate upload for a single run")

    document_sizes = [16 * 1024, 256 * 1024, 1024 * 1024]  # 16kB, 256kB, 1MB
    keyword_counts = [10, 100, 1000]

    # Generate test data
    client = Client()
    consultant = Consultant()

    setup(consultant, [client])

    test_documents = [[os.urandom(document_size) for _ in range(experiment_count)] for document_size in document_sizes]
    test_keywords = [[[os.urandom(8) for _ in range(keyword_count)] for _ in range(experiment_count)] for keyword_count
                     in keyword_counts]

    # perform bandwidth analysis
    for experiment_documents in test_documents:
        print(f"Trying for document sizes: {document_sizes}")
        for experiment_keywords in test_keywords:
            print(f"- Trying for keyword counts: {keyword_counts}")
            bandwidth = 0

            for document, keywords in zip(experiment_documents, experiment_keywords):
                encrypted_document = client.encrypt_data(document, keywords)
                client_id = client.id

                bandwidth += sys.getsizeof(encrypted_document)
                bandwidth += sys.getsizeof(client_id)

            print(bandwidth / experiment_count / 1024)


def evaluate_search_bandwidth():
    experiment_count = 50

    document_counts = [16, 64, 256]
    keyword_counts = [10, 100, 1000]

    # Generate test data
    client = Client()
    consultant = Consultant()
    server = StorageServer()

    setup(consultant, [client])

    # Perform bandwidth analysis
    for dc, kc in product(document_counts, keyword_counts):
        encrypted_documents = [[client.encrypt_data(os.urandom(256 * 1024), [os.urandom(1) for _ in range(kc)]) for _ in range(dc)] for _ in range(experiment_count)]

        bandwidth = 0
        for experiment_documents in encrypted_documents:
            server._storage[client.id] = experiment_documents

            trapdoor = client.create_trapdoor_q(os.urandom(1))

            bandwidth += sys.getsizeof(trapdoor)
            bandwidth += sys.getsizeof(client.id)

            for result in server.keyword_search(trapdoor, client.id):
                bandwidth += sys.getsizeof(result)

        print(f"{dc} documents with {kc} keywords: {bandwidth / experiment_count / 1024 / 1024} MB")


def evaluate_storage_single_user():
    experiment_count = 100

    print("Evaluate server storage for a single user with 20 items")

    document_sizes = [16 * 1024, 256 * 1024, 1024 * 1024]  # 16kB, 256kB, 1MB
    keyword_counts = [10, 100, 1000]

    # Generate test data
    client = Client()
    consultant = Consultant()
    server = StorageServer()

    setup(consultant, [client])

    test_documents = [[os.urandom(document_size) for _ in range(experiment_count)] for document_size in document_sizes]
    test_keywords = [[[os.urandom(8) for _ in range(keyword_count)] for _ in range(experiment_count)] for keyword_count in keyword_counts]

    # perform storage analysis
    for experiment_documents in test_documents:
        print(f"Trying for document sizes: {document_sizes}")
        for experiment_keywords in test_keywords:
            print(f"- Trying for keyword counts: {keyword_counts}")

            for _ in range(20):
                for document, keywords in zip(experiment_documents, experiment_keywords):
                    upload_storage_server_bytes(client, server, document, keywords)

            print(f"{sys.getsizeof(server) / experiment_count / 1024 / 1024} MB")
            server._storage = {}


if __name__ == '__main__':
    # print("> Warm-up run")
    # evaluate_setup_runtime()
    #
    # print("> Actual evaluation")
    #
    # print("|Setup|")
    # evaluate_setup_runtime()
    #
    # print("|Upload|")
    # evaluate_upload_runtime()
    #
    # print("|Search|")
    # evaluate_search_runtime()

    #evaluate_upload_bandwidth()
    #evaluate_search_bandwidth()

    evaluate_storage_single_user()
