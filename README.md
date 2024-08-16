# kbash

`kbash` is a versatile command-line tool designed to manage Kubernetes StatefulSets, Pods, Services, CronJobs, and more. This script provides various options to simplify Kubernetes resource management, making it easier to perform common tasks directly from the command line.

## Prerequisites

- Kubernetes cluster up and running.
- kubectl configured to interact with your Kubernetes cluster.
- Python 3 installed on your system.

## Installation

1. Clone the repository or download the `kbash.py` script to your local machine.
2. Ensure the script is executable:
    ```bash
    chmod +x kbash.py
    ```
3. (Optional) Move the script to `/usr/local/sbin` to make it accessible globally:
    ```bash
    sudo mv kbash.py /usr/local/sbin/kbash
    ```

## Usage

The script provides a variety of options to manage Kubernetes resources. Below are the available commands and their descriptions:

### 1. Rename a StatefulSet
```bash
kbash --rename OLD_STATEFULSET_NAME NEW_STATEFULSET_NAME [--namespace NAMESPACE]
```
- **Description**: Renames an existing StatefulSet.
- **Default Namespace**: `lab`

### 2. Exec into a Pod's Container
```bash
kbash --pod_name POD_NAME [--namespace NAMESPACE] [--container_name CONTAINER_NAME]
```
- **Description**: Executes a shell into the specified container within a pod.
- **Default Container Name**: `user-shell-container`
- **Default Namespace**: `lab`

### 3. List all `kbash` Managed Containers
```bash
kbash --list [--namespace NAMESPACE]
```
- **Description**: Lists all containers labeled with `kbash=true`.
- **Default Namespace**: `lab`

### 4. List all `kbash` Managed StatefulSets
```bash
kbash --stateful [--namespace NAMESPACE]
```
- **Description**: Lists all StatefulSets labeled with `kbash=true`.
- **Default Namespace**: `lab`

### 5. Create a StatefulSet
```bash
kbash --run NAME CONTAINER_PATH [--namespace NAMESPACE]
```
- **Description**: Creates a StatefulSet with the specified name and container path.
- **Default Namespace**: `lab`

### 6. Show All Uniquely Used Containers
```bash
kbash --show-containers [--namespace NAMESPACE]
```
- **Description**: Displays all unique containers used within pods labeled with `kbash=true`.
- **Default Namespace**: `lab`

### 7. Delete a StatefulSet
```bash
kbash --delete NAME [--namespace NAMESPACE]
```
- **Description**: Deletes the specified StatefulSet.
- **Default Namespace**: `lab`

### 8. List All CronJobs Labeled `kbash`
```bash
kbash --job-list [--namespace NAMESPACE]
```
- **Description**: Lists all CronJobs labeled with `kbash=true`.
- **Default Namespace**: `lab`

### 9. Create a CronJob
```bash
kbash --job-run NAME CONTAINER_PATH CRON_SCHEDULE [--namespace NAMESPACE]
```
- **Description**: Creates a CronJob with the specified name, container image, and cron schedule.
- **Default Namespace**: `lab`

### 10. Scale a StatefulSet
```bash
kbash --scale NAME NUMBER [--namespace NAMESPACE]
```
- **Description**: Scales the specified StatefulSet to the desired number of replicas.
- **Default Namespace**: `lab`

### 11. Add a Service for a Pod
```bash
kbash --add-service PODNAME [--type TYPE] [--namespace NAMESPACE]
```
- **Description**: Creates a service for the specified pod.
- **Default Service Type**: `ClusterIP`
- **Alternate Service Type**: `NodePort` (use `--type NodePort`)
- **Default Namespace**: `lab`

### 12. Delete a Service
```bash
kbash --delete-service SERVICENAME [--namespace NAMESPACE]
```
- **Description**: Deletes the specified service.
- **Default Namespace**: `lab`

### 13. Change the Type of an Existing Service
```bash
kbash --service-type SERVICENAME NEW_TYPE [--namespace NAMESPACE]
```
- **Description**: Changes the type of an existing service (e.g., `ClusterIP` to `NodePort`).
- **Default Namespace**: `lab`

## Examples

1. **Rename a StatefulSet**:
    ```bash
    kbash --rename old-name new-name
    ```

2. **Exec into a Pod**:
    ```bash
    kbash --pod_name my-pod
    ```

3. **List All `kbash` Managed StatefulSets**:
    ```bash
    kbash --stateful
    ```

4. **Create a CronJob**:
    ```bash
    kbash --job-run my-job nginx:latest "*/5 * * * *"
    ```

5. **Add a NodePort Service for a Pod**:
    ```bash
    kbash --add-service my-pod --type NodePort
    ```

6. **Scale a StatefulSet**:
    ```bash
    kbash --scale my-statefulset 3
    ```

7. **Delete a Service**:
    ```bash
    kbash --delete-service my-service
    ```

## Contributing

Feel free to submit issues or pull requests to improve this tool. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

