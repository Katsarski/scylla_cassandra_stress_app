import argparse
import re


class CommandLineParser:
    """
    A class to parse command-line arguments.
    """

    @staticmethod
    def parse_args() -> argparse.Namespace:
        """
        Parses command-line arguments.

        :return Parsed arguments.
        """
        parser = argparse.ArgumentParser(description="Concurrent stress test runner and analyzer.")
        parser.add_argument('-d', '--duration', type=str, required=True, help="List of durations/concurrent stress tests (format: 1s,5m,10s)")
        parser.add_argument('-n', '--container_name', type=str, required=False, default="some-scylla",
                            help="Name of the ScyllaDB container.")
        args = parser.parse_args()

        durations = args.duration.split(',')

        # Check if the given duration is in the expected format e.g. 25s,25m,25h
        expected_pattern = r"^(\d+[smh])(,\d+[smh])*$"
        for duration in durations:
            if not re.match(expected_pattern, duration):
                raise ValueError("Invalid duration format. Please provide a list of durations in the " \
                                 "format: 25s,25m,25h")

        return args
