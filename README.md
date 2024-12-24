# Scylla Cassandra Stress Test Application

- NOTE: I've noticed that cassandra-stress shall be run inside the ScyllaDB container itself, however I couldn't locate the stress test application inside so I've modified the solution to use and spin up another container (scylladb/cassandra-stress) that is invoked to generate the load. I think this approach has some advantages - mainly when stress testing the ScyllaDB container instance the resources of that container are not shared with the stress test application/container which will eventually result in more realistic results.

This repository contains a Python application designed to run concurrent stress tests on a ScyllaDB instance running inside a Docker container. The application collects and aggregates performance metrics such as operation rate, mean latency, 99th percentile latency, and maximum latency from all test instances.

## Project Structure

- `stress_test_runner.py`: Main module to run the stress tests.
- `stats.py`: Module to collect, aggregate, and print performance metrics.
- `container.py`: Module to interact with Docker containers.

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

## Usage

1. Start a ScyllaDB container:
    ```sh
    docker run --name some-scylla --hostname some-scylla -d scylladb/scylla --smp 1 --developer-mode 1
    ```

2. Run the stress test:
    ```sh
    cd scylla_cassandra_stress_app
    python stress_test_runner.py -d 1s,5m,10s -n your_scylladb_container_name
    ```

    - `-d`: List of durations for the stress tests (e.g., `1s,5m,10s`).
    - `-n`: Name of the ScyllaDB container (default: `some-scylla`).

## Example

```sh
python stress_test_runner.py -d 30s,1m -n some-scylla
```

This command will run two stress tests concurrently with durations of 30 seconds and 1 minute against the container named `some-scylla`.

## Output

The application will print the aggregated results to the console and save them to a file in the `Results` directory. The results include:

- Number of stress processes that ran
- Start, End time, and overal duration of each process
- Start, End time, and overall duration of the whole test
- Total operation rate (in op/s)
- Average latency mean (in ms)
- Average 99th percentile latency (in ms)
- Standard deviation of maximum latency (in ms)