#!/usr/bin/env python3
import subprocess

def kexec_and_run_bash(namespace, pod_name, container_name):
    try:
        command = [
            'kubectl', 'exec', '-it', pod_name, '-n', namespace, '-c', container_name,
            '--', 'bash', '-c', f'mkdir -p /home/user/{pod_name} && cd /home/user/{pod_name} && exec bash || exec bash'
        ]
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Error executing bash in the container: {e}")
        print(f"Failed to run bash in pod '{pod_name}' with container '{container_name}' in namespace '{namespace}'.")
        print(f"Make sure that the pod name, container name, and namespace are correct and that the container supports running bash.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

