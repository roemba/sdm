import os
import time
import statistics
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
    print(f"Evaluate setup runtime for client counts {client_counts}, performing {experiment_count} of "
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
        for experiment_keywords in test_keywords:
            start = time.monotonic()

            for document, keywords in zip(experiment_documents, experiment_keywords):
                upload_storage_server_bytes(client, server, document, keywords)
                server._storage = {}

            runtime = (time.monotonic() - start) / experiment_count * 1000
            print(runtime)


def evaluate_search_runtime():
    experiment_count = 100
    run_count = 100
    client_counts = [5, 10, 15, 20, 25]
    document_counts = [16, 64, 256]
    keyword_counts = [10, 100, 1000]


if __name__ == '__main__':
    #evaluate_setup_runtime()
    evaluate_upload_runtime()
