#!/usr/bin/env python3
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

