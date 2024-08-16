#!/usr/bin/env python3
import subprocess
import sys

def kexec_and_run_bash(namespace, pod_name, container_name):
    # Derive the username from the pod name
    user_dir = pod_name.split('-')[0]  # Assume the pod name is in the format "<username>-<statefulset-name>-<index>"
    
    try:
        # Construct the kubectl exec command with directory creation if it doesn't exist
        command = [
            "kubectl", "exec", "-it",
            pod_name,
            "-n", namespace,
            "-c", container_name,
            "--", "bash", "-c", f"mkdir -p /home/user/{user_dir} && cd /home/user/{user_dir} && exec bash"
        ]
        
        # Execute the command
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing bash in the container: {e}", file=sys.stderr)
        sys.exit(1)

