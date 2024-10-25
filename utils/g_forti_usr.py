import requests
import json
import urllib3

# Disable SSL warnings (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# FortiGate details
api_key = 'rhpgyj90dj95zg1rGn3gwnsHcgfHQn'
fortigate_ip = '192.168.166.1'  # Replace with your FortiGate's IP address

# Endpoints for API calls
user_url = f'https://{fortigate_ip}/api/v2/cmdb/user/local'
group_url = f'https://{fortigate_ip}/api/v2/cmdb/user/group/edari-access'

# Set up headers for API key authentication
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Define the user data with correct fields for email and two-factor authentication
user_data = {
    "name": "2223344",  # Username for the new user
    "passwd": "mypass",  # Set the user's password
    "email-to": "a@b.com",  # Email address for two-factor authentication
    "two-factor": "email",  # Enable email-based two-factor authentication
    "status": "enable",  # User account status: enable or disable
    "auth-concurrent": "disable"  # Disable concurrent authentication
}

# Function to create the user
def create_user():
    response = requests.post(user_url, headers=headers, json=user_data, verify=False)
    if response.status_code == 200:
        return response.json()  # Successful response
    else:
        return f"Error {response.status_code}: {response.text}"

# Function to add the user to the "edari-access" group
def add_user_to_group(username):
    # Group data to update the group membership
    group_data = {
        "member": [
            {
                "name": username  # The username to add to the group
            }
        ]
    }
    
    response = requests.put(group_url, headers=headers, json=group_data, verify=False)
    
    if response.status_code == 200:
        return response.json()  # Successful response
    else:
        return f"Error {response.status_code}: {response.text}"

# Main script
if __name__ == "__main__":
    # Create the user
    result = create_user()
    print("Create User Response:", json.dumps(result, indent=4))
    
    # If the user creation was successful, add the user to the group
    if 'name' in user_data:
        group_result = add_user_to_group(user_data['name'])
        print("Add User to Group Response:", json.dumps(group_result, indent=4))

