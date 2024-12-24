"""
This module provides the Container class to interact with Docker containers.
"""

import subprocess

class Container:
    """
    A class to interact with Docker containers.
    """

    @staticmethod
    def get_container_ip(container_name: str) -> str:
        """
        Queries for the IP address of of a container given its name.

        :param container_name: The name of the container to get the IP address for
        :param subprocess_module: The subprocess module to execute the stress test command on

        :return The IP address of the ScyllaDB running container
        """

        command = f"docker inspect --format '{{{{.NetworkSettings.IPAddress}}}}' {container_name}"

        try:
            ip = subprocess.check_output(command, shell=True).decode().strip()
        except subprocess.CalledProcessError as ex:
            raise RuntimeError(f"Failed to get the IP address of the ScyllaDB container named: {container_name} "
                                f"(make sure such container is up and running), exception: {ex}") from ex
        except Exception as ex:
            raise RuntimeError(f"Unexpected error occurred while trying to get the IP address of the container "
                                f"named: {container_name}, exception: {ex}") from ex

        if not ip:
            raise ValueError(f"Failed to extract the IP address for container: {container_name}")

        return ip
