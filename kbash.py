#!/usr/bin/env python3
import argparse
from kbash_bash import kexec_and_run_bash
from kbash_rename import rename_statefulset
from kbash_list import list_kbash_containers, list_kbash_statefulsets
from kbash_run import create_stateful_set
from kbash_show_containers import show_kbash_containers  # Import the function

def main():
    parser = argparse.ArgumentParser(description="Manage kbash StatefulSets and Pods.")
    parser.add_argument("--rename", nargs=2, metavar=('OLD_STATEFULSET_NAME', 'NEW_STATEFULSET_NAME'), help="Rename the StatefulSet from OLD_STATEFULSET_NAME to NEW_STATEFULSET_NAME.")
    parser.add_argument("--namespace", default="lab", help="The namespace where the StatefulSet is located (default: 'lab').")
    parser.add_argument("--pod_name", help="The name of the Pod to exec into.")
    parser.add_argument("--container_name", default="user-shell-container", help="The container name within the Pod to exec into (default: 'user-shell-container').")
    parser.add_argument("--list", action="store_true", help="List all kbash managed containers.")
    parser.add_argument("--stateful", action="store_true", help="List all kbash managed StatefulSets.")
    parser.add_argument("--run", nargs=2, metavar=('NAME', 'CONTAINER_PATH'), help="Create a StatefulSet with the given NAME and CONTAINER_PATH.")
    parser.add_argument("--show-containers", action="store_true", help="Show all uniquely used containers with label 'kbash'.")

    args = parser.parse_args()

    if args.rename:
        old_statefulset_name, new_statefulset_name = args.rename
        rename_statefulset(args.namespace, old_statefulset_name, new_statefulset_name)
    elif args.pod_name:
        kexec_and_run_bash(args.namespace, args.pod_name, args.container_name)
    elif args.list:
        list_kbash_containers(args.namespace)
    elif args.stateful:
        list_kbash_statefulsets(args.namespace)
    elif args.run:
        name, container_image = args.run
        create_stateful_set(args.namespace, name, container_image)
    elif args.show_containers:
        show_kbash_containers(args.namespace)
    else:
        print("Error: You must provide a valid argument. Use --help to see available options.")

if __name__ == "__main__":
    main()

