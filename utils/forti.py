import requests
import json

# FortiGate details
api_key = "rhpgyj90dj95zg1rGn3gwnsHcgfHQn"
fortigate_ip = "192.168.166.1"  # Replace with your FortiGate's IP address
url = f"https://{fortigate_ip}/api/v2/"

# Set up headers for API key authentication
headers = {"Authorization": f"Bearer {api_key}"}


# Example 1: Get system status
def get_system_status():
    endpoint = "monitor/system/status"
    response = requests.get(url + endpoint, headers=headers, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error {response.status_code}: {response.text}"


# Example 2: Get a list of firewall policies
def get_firewall_policies():
    endpoint = "cmdb/firewall/policy"
    response = requests.get(url + endpoint, headers=headers, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error {response.status_code}: {response.text}"


# Main script
if __name__ == "__main__":
    # Get system status
    system_status = get_system_status()
    print("System Status:", json.dumps(system_status, indent=4))

    # Get firewall policies
    firewall_policies = get_firewall_policies()
    print("Firewall Policies:", json.dumps(firewall_policies, indent=4))
