import requests
import json
import urllib3

# Disable SSL warnings (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# FortiGate details
api_key = 'rhpgyj90dj95zg1rGn3gwnsHcgfHQn'
fortigate_ip = '192.168.166.1'  # Replace with your FortiGate's IP address
url = f'https://{fortigate_ip}/api/v2/cmdb/user/local'

# Set up headers for API key authentication
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Define the user data with correct fields for email and two-factor authentication
# user_data = {
#     "name": "2223344",  # Username for the new user
#     "passwd": "mypass",  # Set the user's password
#     "email-to": "a@b.com",  # Email address for two-factor authentication
#     "two-factor": "email",  # Enable email-based two-factor authentication
#     "status": "enable",  # User account status: enable or disable
#     "group": ["edari-access"],  # Add user to the 'edari-access' group
#     "auth-concurrent": "disable"  # Disable concurrent authentication
# }

# Function to create the user
def create_forti_user(user_data):
    response = requests.post(url, headers=headers, json=user_data, verify=False)
    
    if response.status_code == 200:
        return  True  #response.json()  # Successful response
    else:
        return False #f"Error {response.status_code}: {response.text}"

# Main script
#"https://<fortigate-ip>/api/v2/cmdb/user/local/{username}"

def modify_forti_user(username, new_password):
    url = f"{url}/{username}"
    data = {
        "passwd": new_password
    }
    response = requests.put(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        print(f"User '{username}' modified successfully.")
    else:
        print(f"Failed to modify user '{username}': {response.text}")

def delete_forti_user(username):
    url1 = f"{url}/{username}"
    response = requests.delete(url1, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"User '{username}' deleted successfully.")
        return True
    else:
        print(f"Failed to delete user '{username}': {response.text}")
        return False


'''
import requests

# Set up the FortiGate details
BASE_URL = "https://<fortigate-ip>/api/v2"
API_KEY = "your_api_key_here"
HEADERS = {
    'Authorization': f'Bearer {API_KEY}'
}

# Disable SSL warnings if necessary (not recommended for production)
requests.packages.urllib3.disable_warnings()

def create_user(username, password):
    url = f"{BASE_URL}/cmdb/user/local"
    data = {
        "name": username,
        "passwd": password,
        "type": "password"  # or "ldap" for LDAP users
    }
    response = requests.post(url, headers=HEADERS, json=data, verify=False)
    if response.status_code == 200:
        print(f"User '{username}' created successfully.")
    else:
        print(f"Failed to create user '{username}': {response.text}")


# Example Usage
create_user("testuser", "password123")
modify_user("testuser", "newpassword456")
delete_user("testuser")


###############

import requests

# Set up the FortiGate details
BASE_URL = "https://<fortigate-ip>/api/v2"
API_KEY = "your_api_key_here"
HEADERS = {
    'Authorization': f'Bearer {API_KEY}'
}

# Disable SSL warnings if necessary (not recommended for production)
requests.packages.urllib3.disable_warnings()

'''
def forti_can_manage_users():
    
    """Check if the API key has permission to list users, indicating user management access."""
    url = f"https://{fortigate_ip}/api/v2/cmdb/user/local"
    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code == 200:
        print("API key has permission to manage users.")
        return True
    elif response.status_code == 403:
        print("Permission denied: API key does not have permission to manage users.")
        return False
    else:
        print(f"Failed to connect to FortiGate: {response.status_code} - {response.text}")
        return False

def forti_user_exists(username):
    """Check if a user with the given username already exists on the FortiGate."""
    BASE_URL=f'https://{fortigate_ip}'
    url = f"{BASE_URL}/cmdb/user/local/{username}"
    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code == 200:
        print(f"User '{username}' already exists.")
        return True
    elif response.status_code == 404:
        print(f"User '{username}' does not exist and can be created.")
        return False
    else:
        print(f"Error checking user existence: {response.status_code} - {response.text}")
        return False

# Usage
# if can_manage_users():
#     username = "testuser"
#     if not user_exists(username):
#         print("It is possible to create the user.")
#     else:
#         print("The user already exists; consider modifying instead of creating.")
# else:
#     print("User management is not allowed with the current API key.")

