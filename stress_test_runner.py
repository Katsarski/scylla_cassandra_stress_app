"""
This module provides functionality to run a concurrent stress test on Cassandra using Docker,
parse the results, and aggregate the statistics.
"""

import argparse
import subprocess
import concurrent.futures
import re
from datetime import datetime
from stats import Stats
from container import Container

class StressTestRunner:
    """
    A class to run a stress test on Cassandra and collect performance metrics.

    This class runs the `cassandra-stress` tool in a Docker container and extracts performance 
    metrics such as operation rate, mean latency, 99th percentile latency, and maximum latency.
    """

    def __init__(self, duration: str, container_name: str) -> None:
        """
        :param duration: The duration for which the stress test should run.
        """
        self.duration = duration
        self.container_name = container_name
        self.start_time = None
        self.end_time = None
        self.result = None

    def run(self) -> dict:
        """
        Runs the `cassandra-stress` command and captures the output.

        :return Dictionary containing parsed performance metrics
        """
        threads = 10
        command = f'docker run --rm scylladb/cassandra-stress "cassandra-stress write duration={self.duration} ' \
                  f'-rate threads={threads} -node {Container.get_container_ip(self.container_name)}"'

        self.start_time = datetime.now()
        print(f"Running stress test with threads: {threads}, duration: {self.duration} against " \
              f"container {self.container_name} ...")

        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.end_time = datetime.now()

        self.result = Stats.parse_run_output(result.stdout.decode(), self.start_time, self.end_time)
        return self.result

def main() -> None:
    """
    The main function that parses command-line arguments, runs the stress tests, 
    and aggregates the results.

    This function runs multiple stress tests concurrently using `ThreadPoolExecutor`, and prints aggregated 
    results after the tests are completed.
    """
    parser = argparse.ArgumentParser(description="Concurrent stress test runner and analyzer.")
    parser.add_argument('-d', '--duration', type=str, help="List of durations (format: 1s,5m,10s)", required=True)
    parser.add_argument('-n', '--container_name', type=str, help="ScyllaDb container name defaults to some-scylla",
                        required=False, default="some-scylla")

    args = parser.parse_args()
    durations = args.duration.split(',')

    # Use re.match to check if the given duration is in the expected format e.g. 25s,25m,25h
    expected_pattern = r"^(\d+[smh])(,\d+[smh])*$"
    for duration in durations:
        if not re.match(expected_pattern, duration):
            raise ValueError("Invalid duration format. Please provide a list of durations in the format: 25s,25m,25h")

    stats = Stats()

    # Run N stress tests concurrently based on the number of durations provided (N = len(durations))
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(durations)) as executor:
        # Create a list containing StressTestRunner objects - one for each duration provided
        runners = [StressTestRunner(duration, args.container_name) for duration in durations]

        futures = [executor.submit(runner.run) for runner in runners]
        finished = 0

        # Fill in the statistics object with results from the runs
        for future in concurrent.futures.as_completed(futures):
            finished += 1
            print(f"Finished {finished}/{len(durations)}")
            runner_result = future.result()
            stats.add(runner_result)

    stats.output_aggregated_results(stats)

if __name__ == "__main__":
    main()
