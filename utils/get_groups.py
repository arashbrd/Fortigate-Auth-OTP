# import requests
# import json
# import urllib3

# # Disable SSL warnings (not recommended for production)
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# # FortiGate details
# api_key ='rhpgyj90dj95zg1rGn3gwnsHcgfHQn'
# fortigate_ip = '192.168.166.1'  # Replace with your FortiGate's IP address
# url = f'https://{fortigate_ip}/api/v2/cmdb/user/group'

# # Set up headers for API key authentication
# headers = {
#     'Authorization': f'Bearer {api_key}',
#     'Content-Type': 'application/json'
# }

# # Function to retrieve all user groups
# def get_user_groups():
#     response = requests.get(url, headers=headers, verify=False)

#     if response.status_code == 200:
#         return response.json()  # Return the user groups if successful
#     else:
#         return f"Error {response.status_code}: {response.text}"

# # Main script
# if __name__ == "__main__":
#     groups = get_user_groups()
#     print("User Groups:", json.dumps(groups, indent=4))
import os
import requests
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

# Retrieve values from .env file
api_key = os.getenv("FORTIGATE_API_KEY")
fortigate_ip = os.getenv("FORTIGATE_IP")
# FortiGate details
# api_key = 'rhpgyj90dj95zg1rGn3gwnsHcgfHQn'  # Replace with your API key
# fortigate_ip = '192.168.166.1'  # Replace with your FortiGate's IP address
url = f"https://{fortigate_ip}/api/v2/cmdb/user/group"

# Set up headers for API key authentication
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


# Function to retrieve all user groups and return only their names
def get_user_group_names():
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        # Extract the "results" list and retrieve only the "name" field from each entry
        groups = response.json().get("results", [])
        group_names = [group["name"] for group in groups]
        group_ids = [group["id"] for group in groups]
        return group_names, group_ids
    else:
        return f"Error {response.status_code}: {response.text}"


# Main script
if __name__ == "__main__":
    group_names, group_ids = get_user_group_names()
    print("User Group Names:", group_names)
    print("+++++++++++++++")
    print("User Group Names:", group_ids)
