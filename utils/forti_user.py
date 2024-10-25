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
user_data = {
    "name": "2223344",  # Username for the new user
    "passwd": "mypass",  # Set the user's password
    "email-to": "a@b.com",  # Email address for two-factor authentication
    "two-factor": "email",  # Enable email-based two-factor authentication
    "status": "enable",  # User account status: enable or disable
    "group": ["edari-access"],  # Add user to the 'edari-access' group
    "auth-concurrent": "disable"  # Disable concurrent authentication
}

# Function to create the user
def create_user():
    response = requests.post(url, headers=headers, json=user_data, verify=False)
    
    if response.status_code == 200:
        return response.json()  # Successful response
    else:
        return f"Error {response.status_code}: {response.text}"

# Main script
if __name__ == "__main__":
    # Create the user
    result = create_user()
    print("Create User Response:", json.dumps(result, indent=4))

