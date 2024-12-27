import subprocess
from datetime import datetime
from utils.stats import Stats
from utils.container import Container

class StressTestRunner:
    """
    A class to run a stress test and collect performance metrics.

    This class runs the `cassandra-stress` tool in a Docker container and extracts performance 
    metrics
    """

    def __init__(self, duration: str, container_name: str) -> None:
        """
        :param duration: The duration(s)/amounts of stress tests to run.
        :param container_name: The name of the ScyllaDB container.
        """
        self.duration = duration
        self.container_name = container_name
        self.start_time = None
        self.end_time = None
        self.result = None

    def run_stress_test(self) -> dict:
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

        self.result = Stats.parse_result_output(result.stdout.decode(), self.start_time, self.end_time)
        return self.result
