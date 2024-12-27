from parsers.command_line_parser import CommandLineParser
from runners.stress_test_manager import StressTestManager


def main() -> None:
    """
    The main function that parses command-line arguments, runs the stress tests, 
    and aggregates the results.
    """
    args = CommandLineParser.parse_args()
    manager = StressTestManager(args.duration.split(','), args.container_name)
    manager.run_concurrent_stress_tests()

if __name__ == "__main__":
    main()
