import subprocess
import json

import subprocess
import json

def list_kbash_cronjobs(namespace="lab"):
    try:
        # Get all CronJobs with the label 'kbash'
        command = [
            'kubectl', 'get', 'cronjobs', '-n', namespace,
            '-l', 'kbash=true', '-o', 'json'
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error retrieving CronJobs: {result.stderr}")
            return

        cronjobs = json.loads(result.stdout)
        if cronjobs.get('items'):
            print("Kubernetes CronJobs with label 'kbash':")
            for cronjob in cronjobs.get('items', []):
                print(f"- {cronjob['metadata']['name']}")
        else:
            print("No CronJobs found with the label 'kbash'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_kbash_cronjob(namespace, name, container_image, command, schedule):
    cronjob_yaml = f"""
apiVersion: batch/v1
kind: CronJob
metadata:
  name: {name}
  labels:
    kbash: "true"
spec:
  schedule: "{schedule}"
  jobTemplate:
    spec:
      template:
        metadata:
          labels:
            kbash: "true"
        spec:
          containers:
          - name: {name}-container
            image: {container_image}
            command: {command}
          restartPolicy: OnFailure
    """
    try:
        process = subprocess.Popen(['kubectl', 'apply', '-f', '-'], stdin=subprocess.PIPE)
        process.communicate(input=cronjob_yaml.encode())
        print(f"CronJob '{name}' created with container '{container_image}' and schedule '{schedule}' in namespace '{namespace}'.")
    except Exception as e:
        print(f"An error occurred while creating the CronJob: {e}")

