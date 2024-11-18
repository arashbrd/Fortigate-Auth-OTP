import requests
import urllib3
import logging
import json

logger = logging.getLogger("db")
from core.settings import FORTIGATE_API_KEY
from core.settings import FORTIGATE_IP

# FortiGate details
api_key = FORTIGATE_API_KEY
fortigate_ip = f"https://{FORTIGATE_IP}/"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up headers for API key authentication
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def create_user_600d(user_data):
    print("Creating user for FortiGate 400F...")
    # Specific logic for 400F
    user_endpoint = "api/v2/cmdb/user/local"
    response = requests.post(
        fortigate_ip + user_endpoint,
        headers=headers,
        data=json.dumps(user_data),
        verify=False,
    )
    if response.status_code == 200 and response.json().get("status") == "success":
        print("User created successfully on FortiGate 400F.")
    else:
        print("Failed to create user on FortiGate 400F.")
        print(response.text)
        logger.error(f"User created successfully on FortiGate 400F.{response.text}")


# Specific implementation for FortiGate 600D


def modify_forti_user_600d(username, user_group, status):
    print("**********************************")
    print(f"username={username}, user_group={user_group}, status={status}")
    print("**********************************")
    user_endpoint = f"api/v2/cmdb/user/local/{username}"

    # url1 = f"{user_endpoint}/{username}"
    data = {"status": status, "user_group": [user_group]}
    response = requests.put(
        fortigate_ip + user_endpoint, headers=headers, json=data, verify=False
    )
    if response.status_code == 200:
        print(f"User '{username}' modified successfully.")
        logger.info(f"User '{username}' modified successfully.")
        return True
    else:
        print(f"Failed to modify user '{username}': {response.text}")
        logger.error(f"Failed to modify user '{username}': {response.text}")
        return False


def delete_forti_user_600d(username):
    user_endpoint = f"api/v2/cmdb/user/local/{username}"

    # url1 = f"{user_endpoint}/{username}"
    response = requests.delete(
        fortigate_ip + user_endpoint, headers=headers, verify=False
    )
    if response.status_code == 200:
        print(f"User '{username}' deleted successfully.")
        logger.info(f"User '{username}' deleted successfully.")
        return True
    else:
        logger.error(f"Failed to delete user '{username}': {response.text}")
        print(f"Failed to delete user '{username}': {response.text}")
        return False
