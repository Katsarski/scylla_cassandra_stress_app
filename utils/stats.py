import datetime
import os
import re
import statistics

class Stats:
    """
    A class for collecting, aggregating, and printing/storing performance metrics gathered during stress test(s).
    """

    def __init__(self) -> None:
        """
        Initializes an instance of the Stats class to collect performance metrics.
        """
        self.op_rates = []
        self.latency_means = []
        self.latency_99ths = []
        self.latency_max = []
        self.start_times = []
        self.end_times = []

    def add(self, result: dict) -> None:
        """
        This method appends values for operation rate, latency mean, 99th percentile latency, 
        max latency, start time, and end time from the given stress test run instance.

        :param result: A dictionary containing the performance metrics to be added.
        """
        self.op_rates.append(result["op_rate"])
        self.latency_means.append(result["latency_mean"])
        self.latency_99ths.append(result["latency_99th"])
        self.latency_max.append(result["latency_max"])
        self.start_times.append(result["start_time"])
        self.end_times.append(result["end_time"])

    def aggregate_results(self) -> dict:
        """
        Aggregates the performance metrics from all added stress test run results.

        :return A dictionary containing the performance results:
        """
        total_op_rate = sum(self.op_rates)
        avg_latency_mean = sum(self.latency_means) / len(self.latency_means)
        avg_latency_99th = sum(self.latency_99ths) / len(self.latency_99ths)
        stddev_latency_max = statistics.stdev(self.latency_max)
        start_time = min(self.start_times)
        end_time = max(self.end_times)

        return {
            "total_op_rate": total_op_rate,
            "avg_latency_mean": avg_latency_mean,
            "avg_latency_99th": avg_latency_99th,
            "stddev_latency_max": stddev_latency_max,
            "start_time": start_time,
            "end_time": end_time,
            "total_duration": end_time - start_time
        }

    @staticmethod
    def output_aggregated_results(stats: "Stats") -> None:
        """
        Stores and prints the aggregated results in a human-readable format, including individual
        process start time, end time, and duration, prints and saves the results to a file.
        """
        results_dir = "Results"
        os.makedirs(results_dir, exist_ok=True)

        # Format the results filename with the start and end times of the current run
        start_time_str = min(stats.start_times).strftime("%Y-%m-%d_%H-%M-%S")
        end_time_str = max(stats.end_times).strftime("%Y-%m-%d_%H-%M-%S")
        results_filename = f"{results_dir}/Start_{start_time_str}_End_{end_time_str}.txt"

        # Write results to the file
        with open(results_filename, "w", encoding="utf-8") as f:
            f.write("Aggregated Results:\n")
            f.write(f"Number of stress processes that ran: {len(stats.op_rates)}\n")

            # Also write details for each individual process/run
            for i, (start_time, end_time) in enumerate(zip(stats.start_times, stats.end_times), start=1):
                duration = end_time - start_time
                f.write(f"\nProcess {i}:\n")
                f.write(f"  Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"  End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"  Duration: {str(duration).split('.', maxsplit=1)[0]}\n")

            # Also write the overall aggregated results
            f.write("\nTest aggregated results:\n")
            f.write(f"Start time: {min(stats.start_times).strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"End time: {max(stats.end_times).strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Test duration: {str(max(stats.end_times) - min(stats.start_times)).split('.', maxsplit=1)[0]}\n")
            f.write(f"Aggregation of Op rate (sum): {stats.aggregate_results()['total_op_rate']} op/s\n")
            f.write(f"Average of Latency mean: {stats.aggregate_results()['avg_latency_mean']:.3f} ms\n")
            f.write(f"Average of Latency 99th percentile: {stats.aggregate_results()['avg_latency_99th']:.3f} ms\n")
            f.write(f"Standard deviation of Latency max: {stats.aggregate_results()['stddev_latency_max']:.3f} ms\n")

        with open(results_filename, "r", encoding="utf-8") as file:
            file_content = file.read()
            print("\nResults: \n")
            print(file_content)
        print(f"Results saved to {results_filename}")

    @staticmethod
    def parse_result_output(output: str, instance_start_time: datetime, instance_end_time: datetime) -> dict:
        """
        Parses the output of the stress test command and extracts relevant statistics.

        :param output: The raw output from the `cassandra-stress` command.
        :param instance_start_time: The start date/time of the stress test instance.
        :param instance_end_time: The end date/time of the stress test instance.
        :return Dictionary containing the performance metrics
        """
        # Regex patterns to extract needed metrics
        op_rate_pattern = r"Op rate\s*:\s*([\d,]+)\s*op/s"
        latency_mean_pattern = r"Latency mean\s*:\s*([\d.]+)\s*ms"
        latency_99th_pattern = r"Latency 99th percentile\s*:\s*([\d.]+)\s*ms"
        latency_max_pattern = r"Latency max\s*:\s*([\d.]+)\s*ms"

        op_rate = int(re.search(op_rate_pattern, output).group(1).replace(",", ""))
        latency_mean = float(re.search(latency_mean_pattern, output).group(1))
        latency_99th = float(re.search(latency_99th_pattern, output).group(1))
        latency_max = float(re.search(latency_max_pattern, output).group(1))

        return {
            "op_rate": op_rate,
            "latency_mean": latency_mean,
            "latency_99th": latency_99th,
            "latency_max": latency_max,
            "start_time": instance_start_time,
            "end_time": instance_end_time,
            "duration": instance_end_time - instance_start_time
        }
