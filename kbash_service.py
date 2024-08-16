import subprocess

def create_service(namespace, pod_name, service_name, service_type="ClusterIP"):
    try:
        service_yaml = f"""
apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  labels:
    kbash: "true"
spec:
  selector:
    app: {pod_name}
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: {service_type}
"""
        process = subprocess.Popen(['kubectl', 'apply', '-f', '-'], stdin=subprocess.PIPE)
        process.communicate(input=service_yaml.encode())
        print(f"Service '{service_name}' created for pod '{pod_name}' with type '{service_type}'.")
    except Exception as e:
        print(f"An error occurred while creating the service: {e}")

def delete_service(namespace, service_name):
    try:
        command = ['kubectl', 'delete', 'service', service_name, '-n', namespace]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error deleting service: {result.stderr}")
        else:
            print(f"Service '{service_name}' deleted successfully in namespace '{namespace}'.")
        
    except Exception as e:
        print(f"An error occurred while deleting the service: {e}")

def change_service_type(namespace, service_name, new_type):
    try:
        patch_command = [
            'kubectl', 'patch', 'service', service_name, '-n', namespace,
            '--type=merge', '-p', f'{{"spec": {{"type": "{new_type}"}}}}'
        ]
        result = subprocess.run(patch_command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error changing service type: {result.stderr}")
        else:
            print(f"Service '{service_name}' type changed to '{new_type}' successfully.")
        
    except Exception as e:
        print(f"An error occurred while changing the service type: {e}")

