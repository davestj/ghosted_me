# GhostedMe

GhostedMe is a versatile chaos engineering tool designed to introduce controlled disruptions into Kubernetes clusters by randomly deleting attached volumes and storage resources. Developed for DevOps and SRE teams, GhostedMe adds an element of unpredictability to Kubernetes environments, allowing users to test the resilience and fault tolerance of their applications and infrastructure.

### Features:

- **Random Volume Deletion**: GhostedMe randomly selects an attached volume and deletes it, simulating a failure scenario in the Kubernetes cluster.
  
- **Storage Resource Removal**: In addition to volumes, GhostedMe can also randomly delete associated storage resources, further stressing the cluster's resilience.

- **Detached Volume Mode**: GhostedMe offers a `--timetoghost` flag to detach a volume for a specified amount of time before reattaching it, allowing users to test scenarios where volumes are temporarily unavailable.

### Installation:

To install GhostedMe, follow these steps:

1. **Clone the Repository**: 
    ```bash
    git clone https://github.com/davestj/ghosted_me.git
    ```

2. **Navigate to the Directory**: 
    ```bash
    cd ghosted_me
    ```

3. **Ensure Dependencies**: Make sure you have `kubectl` installed and configured properly on your system.

4. **Run GhostedMe**: Execute the script using Python 3.11.
    ```bash
    python3.11 ghostedme.py
    ```

### Usage:

GhostedMe accepts the following command-line option:

- `--timetoghost`: Detaches the selected volume for a specified amount of time in seconds before reattaching it.

### Embrace Chaos with Mr. Mayhem:

Unleash the chaos engineering prowess of Mr. Mayhem with GhostedMe! Mr. Mayhem, your trusty chaos engineer, is here to help you uncover vulnerabilities and fortify your Kubernetes deployments with a touch of chaos and sophistication.

---

GhostedMe is your companion in chaos engineering, providing valuable insights into the resilience of your Kubernetes clusters while keeping the spirit of Mr. Mayhem alive. Let's embrace chaos responsibly and build more robust and reliable systems together!