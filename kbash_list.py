#!/usr/bin/env python3
from kubernetes import client, config

def list_kbash_containers(namespace):
    config.load_kube_config()
    v1 = client.CoreV1Api()

    try:
        pods = v1.list_namespaced_pod(namespace=namespace, label_selector="kbash=true")
        if not pods.items:
            print("No kbash managed containers found.")
            return

        print("kbash managed containers:")
        for pod in pods.items:
            print(f"- {pod.metadata.name}")
    except client.exceptions.ApiException as e:
        print(f"Failed to list kbash managed containers: {e}")

def list_kbash_statefulsets(namespace):
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

    try:
        statefulsets = apps_v1.list_namespaced_stateful_set(namespace=namespace, label_selector="kbash=true")
        if not statefulsets.items:
            print("No kbash managed StatefulSets found.")
            return

        print("kbash managed StatefulSets:")
        for statefulset in statefulsets.items:
            print(f"- {statefulset.metadata.name}")
    except client.exceptions.ApiException as e:
        print(f"Failed to list kbash managed StatefulSets: {e}")

