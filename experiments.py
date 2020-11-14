import time
import statistics
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


if __name__ == '__main__':
    evaluate_setup_runtime()
