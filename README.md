# Scylla Cassandra Stress Test Application

- NOTE: According to the task description cassandra-stress shall be run inside the ScyllaDB container, however I couldn't locate the cassandra-stress app there so I've improvized and I'm spinning up N (scylladb/cassandra-stress) containers where N == len(stress test(s) duration(s) provided). I think this approach has some advantages - mainly when stress testing the ScyllaDB container instance the resources of that container are not shared with the stress test container(s) which will eventually result in more realistic results. The cassandra-stress containers can also be extended and spined up inside a cluster allowing for even bigger load to be generated avoiding all resources being occupied. The only drawback I see is related to the overall duration of the tests which slightly differs from the provided as command line param durations since spinning up each stress test container creates a several seconds overhead which is added to the total duration of the tests.

This repository contains a Python application designed to run concurrent cassandra-stress tests against a ScyllaDB instance running inside a Docker container. The amount of stress test instances to run are determined based on the amount of comma-separated duration(s) provided. The application collects and aggregates performance metrics such as operation rate, mean latency, 99th percentile latency, and maximum latency from all test instances.

## Project Structure

- `main.py`: Main entry point for the application.
- `parsers/command_line_parser.py`: Module to parse command-line arguments.
- `runners/stress_test_manager.py`: Module to manage the execution of multiple stress tests and aggregate their results.
- `runners/stress_test_runner.py`: Module to run a single stress test and collect performance metrics.
- `utils/stats.py`: Module to collect, aggregate, and print performance metrics.
- `utils/container.py`: Module to interact with Docker containers.

## Requirements

- Python 3.6+ installed
- Docker installed
- ScyllaDB Docker image (`scylladb/scylla`) cloned
- Cassandra stress Docker image (`scylladb/cassandra-stress`) cloned

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Katsarski/scylla_cassandra_stress_app.git
    ```

## Example usage

1. Start a ScyllaDB container:
    ```sh
    docker run --name some-scylla --hostname some-scylla -d scylladb/scylla --smp 1 --developer-mode 1
    ```

2. Run the stress test:
    ```sh
    cd scylla_cassandra_stress_app
    python main.py -d 30s,1m
    ```

    The above command will run two stress tests concurrently with durations of 30 seconds and 1 minute against the container named `some-scylla`.

    - `-d`: List of comma separated duration(s) also controlling the amount of stress test(s) to run (e.g., `25m,1h,50s`).
    - `-n`: Name of the ScyllaDB container (default: `some-scylla`).

## Output

The application will print the aggregated results to the console and save them to a file in the `Results` directory. The results include:

- Number of stress processes that ran
- Start, End time, and overal duration of each process
- Start, End time, and overall duration of the whole test
- Total operation rate (in op/s)
- Average latency mean (in ms)
- Average 99th percentile latency (in ms)
- Standard deviation of maximum latency (in ms)

## Known issues

- Using print() instead of propper logging mechanism
- Error handling can be improved to provide more informative messages and handle edge cases in a better way
- The printed/stored output process/test duration also includes a ~15 seconds overhead due to the time it takes to spin up the `scylladb/cassandra-stress` container
- The printed/stored output process/test duration does not properly round the seconds elapsed time and can differ to up to +1 second (excluding the time it takes to spin up the `scylladb/cassandra-stress` container)