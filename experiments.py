import time
from typing import List

from client import Client
from consultant import Consultant
from protocols import setup
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
    experiment_count = 10000
    client_counts = [5, 10, 15, 20, 25, 30, 45, 50]
    print(f"Evaluate setup runtime for client counts {client_counts}, repeating {experiment_count} times.")

    # Generate test data
    test_data: List[List[SystemSetup]] = []
    for client_count in client_counts:
        test_data.append([SystemSetup(client_count) for _ in range(experiment_count)])

    # Perform runtime analysis
    runtimes = []
    for row in test_data:
        start = time.monotonic()

        for system_setup in row:
            setup(system_setup.consultant, system_setup.clients)

        runtime = (time.monotonic() - start) / experiment_count
        runtimes.append(runtime * 1000)

    print(f"Runtimes: {runtimes} ms")


if __name__ == '__main__':
    evaluate_setup_runtime()
