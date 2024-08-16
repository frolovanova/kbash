
import subprocess

def create_service_if_not_exists(namespace, pod_name, service_name, container_port):
    try:
        # Check if the service already exists
        check_command = [
            'kubectl', 'get', 'service', service_name, '-n', namespace
        ]
        result = subprocess.run(check_command, capture_output=True, text=True)
        
        if result.returncode != 0:
            # Service does not exist, create it
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
      port: {container_port}
      targetPort: {container_port}
"""
            process = subprocess.Popen(['kubectl', 'apply', '-f', '-'], stdin=subprocess.PIPE)
            process.communicate(input=service_yaml.encode())
            print(f"Service '{service_name}' created for pod '{pod_name}' on port {container_port}.")
        else:
            print(f"Service '{service_name}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating the service: {e}")

def port_forward(namespace, pod_name, local_port, container_port):
    service_name = f"{pod_name}-service"
    create_service_if_not_exists(namespace, pod_name, service_name, container_port)

    try:
        command = [
            'kubectl', 'port-forward', f'service/{service_name}', f'{local_port}:{container_port}', '-n', namespace
        ]
        print(f"Forwarding local port {local_port} to container port {container_port} through service '{service_name}'...")
        subprocess.run(command)
    except Exception as e:
        print(f"An error occurred while setting up port forwarding: {e}")

