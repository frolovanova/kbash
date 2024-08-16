import subprocess

def delete_stateful_set(namespace, name):
    try:
        # Delete the StatefulSet
        command = ['kubectl', 'delete', 'statefulset', name, '-n', namespace]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error deleting StatefulSet: {result.stderr}")
        else:
            print(f"StatefulSet '{name}' deleted successfully in namespace '{namespace}'.")
        
    except Exception as e:
        print(f"An error occurred while deleting the StatefulSet: {e}")

