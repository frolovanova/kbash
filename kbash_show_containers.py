import subprocess
import json

def show_kbash_containers(namespace="lab"):
    try:
        # Get all pods with the label 'kbash'
        command = [
            'kubectl', 'get', 'pods', '-n', namespace,
            '-l', 'kbash=true', '-o', 'json'
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error retrieving pods: {result.stderr}")
            return

        pods = json.loads(result.stdout)
        unique_containers = set()

        # Iterate through the pods and collect unique container images
        for pod in pods.get('items', []):
            containers = pod.get('spec', {}).get('containers', [])
            for container in containers:
                unique_containers.add(container.get('image'))

        if unique_containers:
            print("Unique containers used with label 'kbash':")
            for container in unique_containers:
                print(f"- {container}")
        else:
            print("No containers found with the label 'kbash'.")

    except Exception as e:
        print(f"An error occurred: {e}")

