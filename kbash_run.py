import subprocess

def create_stateful_set(namespace, name, container_image):
    stateful_set_yaml = f"""
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: {name}
  labels:
    kbash: "true"
spec:
  serviceName: "{name}-service"
  replicas: 1
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
        kbash: "true"
    spec:
      containers:
      - name: {name}-container
        image: {container_image}
        ports:
        - containerPort: 80
  volumeClaimTemplates:
  - metadata:
      name: {name}-pvc
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 1Gi
    """
    process = subprocess.Popen(['kubectl', 'apply', '-f', '-'], stdin=subprocess.PIPE)
    process.communicate(input=stateful_set_yaml.encode())
    print(f"StatefulSet '{name}' created with container '{container_image}' in namespace '{namespace}'.")

