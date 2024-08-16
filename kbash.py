#!/usr/bin/env python3
import argparse
import subprocess
import sys
from kubernetes import client, config

def is_valid_name(name):
    """Ensure the name is valid for Kubernetes objects."""
    if '.' in name:
        print(f"Error: '{name}' is not a valid Kubernetes object name. It must not contain dots.")
        sys.exit(1)

def rename_statefulset(namespace, old_statefulset_name, new_statefulset_name):
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

    is_valid_name(new_statefulset_name)  # Validate the new StatefulSet name

    try:
        # Get the existing StatefulSet
        statefulset = apps_v1.read_namespaced_stateful_set(name=old_statefulset_name, namespace=namespace)
    except client.exceptions.ApiException as e:
        print(f"Failed to find StatefulSet '{old_statefulset_name}' in namespace '{namespace}': {e}")
        sys.exit(1)

    # Change the StatefulSet name
    statefulset.metadata.name = new_statefulset_name
    statefulset.metadata.resource_version = None  # Resource version must be None when creating a new object

    # Create the new StatefulSet with the updated name
    try:
        apps_v1.create_namespaced_stateful_set(namespace=namespace, body=statefulset)
        print(f"StatefulSet created with name '{new_statefulset_name}'")
    except client.exceptions.ApiException as e:
        print(f"Failed to create new StatefulSet '{new_statefulset_name}': {e}")
        sys.exit(1)

    # Delete the old StatefulSet
    try:
        apps_v1.delete_namespaced_stateful_set(name=old_statefulset_name, namespace=namespace)
        print(f"Old StatefulSet '{old_statefulset_name}' deleted")
    except client.exceptions.ApiException as e:
        print(f"Failed to delete old StatefulSet '{old_statefulset_name}': {e}")

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

def main():
    parser = argparse.ArgumentParser(description="Rename a StatefulSet or exec into a Pod's bash restricted to a user's directory.")
    parser.add_argument("--rename", nargs=2, metavar=('OLD_STATEFULSET_NAME', 'NEW_STATEFULSET_NAME'), help="Rename the StatefulSet from OLD_STATEFULSET_NAME to NEW_STATEFULSET_NAME.")
    parser.add_argument("--namespace", default="lab", help="The namespace where the StatefulSet is located (default: 'lab').")
    parser.add_argument("--pod_name", help="The name of the Pod to exec into.")
    parser.add_argument("--container_name", default="user-shell-container", help="The container name within the Pod to exec into (default: 'user-shell-container').")

    args = parser.parse_args()

    if args.rename:
        old_statefulset_name, new_statefulset_name = args.rename
        rename_statefulset(args.namespace, old_statefulset_name, new_statefulset_name)
    elif args.pod_name:
        # Exec into the pod and start a bash shell restricted to the user's directory
        kexec_and_run_bash(args.namespace, args.pod_name, args.container_name)
    else:
        print("Error: You must provide either --rename to rename a StatefulSet or --pod_name to exec into a Pod's bash.")

if __name__ == "__main__":
    main()

