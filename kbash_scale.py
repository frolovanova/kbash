import subprocess

def scale_stateful_set(namespace, name, replicas):
    try:
        command = [
            'kubectl', 'scale', 'statefulset', name,
            f'--replicas={replicas}', '-n', namespace
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error scaling StatefulSet: {result.stderr}")
        else:
            print(f"StatefulSet '{name}' scaled to {replicas} replicas in namespace '{namespace}'.")
    except Exception as e:
        print(f"An error occurred while scaling the StatefulSet: {e}")

