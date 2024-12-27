import concurrent.futures

from utils.stats import Stats
from runners.stress_test_runner import StressTestRunner


class StressTestManager:
    """
    A class to manage the execution of multiple stress tests and aggregate their results.
    """

    def __init__(self, durations: list, container_name: str) -> None:
        """
        :param durations: List of durations/instances of the stress test(s).
        :param container_name: The name of the ScyllaDB container to test against.
        """
        self.durations = durations
        self.container_name = container_name
        self.stats = Stats()

    def run_concurrent_stress_tests(self) -> None:
        """
        Runs multiple stress tests concurrently and aggregates the results.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.durations)) as executor:
            runners = [StressTestRunner(duration, self.container_name) for duration in self.durations]

            futures = [executor.submit(runner.run_stress_test) for runner in runners]
            finished = 0

            # Fill in the statistics object with results from the runs
            for future in concurrent.futures.as_completed(futures):
                finished += 1
                print(f"Finished {finished}/{len(self.durations)}")
                runner_result = future.result()
                self.stats.add(runner_result)

        self.stats.output_aggregated_results(self.stats)
