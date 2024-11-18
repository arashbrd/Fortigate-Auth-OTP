import requests
import urllib3
import logging
import json
logger = logging.getLogger("db")
from core.settings import FORTIGATE_API_KEY
from core.settings import FORTIGATE_IP
from .forti_utils import get_fortigate_model
from utils.forti.forti_400f.manage_users import (
    create_user_400f,
    delete_forti_user_400f,
    modify_forti_user_400f,
)
from utils.forti.forti_600d.manage_users import (
    create_user_600d,
    delete_forti_user_600d,
    modify_forti_user_600d,
)

# Disable SSL warnings (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# FortiGate details
api_key = FORTIGATE_API_KEY
# fortigate_ip = FORTIGATE_IP  # Replace with your FortiGate's IP address
fortigate_ip = f"https://{FORTIGATE_IP}/"
# url = f"https://{fortigate_ip}/api/v2/cmdb/user/local/"

# Set up headers for API key authentication
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

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


# Function to fetch FortiGate model


# Dispatcher function to handle model-specific logic
def create_forti_user(user_data):
    # Fetch FortiGate system details
    model = get_fortigate_model()
    print("#############################")
    print(f"model is {model}")
    print("#############################")

    # Dispatch to the appropriate function based on the model
    if model == "400F":
        return create_user_400f(user_data)
    elif model == "600D":
        return create_user_600d(user_data)


# Function to create the user
# def create_forti_user(user_data):

#     response = requests.post(url, headers=headers, json=user_data, verify=False)

#     if response.status_code == 200:
#         logger.info(f"User '{user_data["name"]}' created  successfully.")
#         return True  # response.json()  # Successful response
#     else:
#         logger.info(
#             f"User '{user_data["name"]}' created  failed.response.status_code={response.status_code}"
#         )
#         return False  # f"Error {response.status_code}: {response.text}"


# Main script
# "https://<fortigate-ip>/api/v2/cmdb/user/local/{username}"
def modify_forti_user(username, user_group, status):
    # Fetch FortiGate system details
    model = get_fortigate_model()

    # Dispatch to the appropriate function based on the model
    if model == "400F":
        return modify_forti_user_400f(username, user_group, status)
    elif model == "600D":
        return modify_forti_user_600d(username, user_group, status)


# Fetch FortiGate system details
def delete_forti_user(username):
    model = get_fortigate_model()

    # Dispatch to the appropriate function based on the model
    if model == "400F":
        return delete_forti_user_400f(username)
    elif model == "600D":
        return delete_forti_user_600d(username)


def assign_forti_user_to_group(username, group_name):
    group_endpoint = f"api/v2/cmdb/user/local/{group_name}"
    # url = f"https://{fortigate_ip}/api/v2/cmdb/user/group/{group_name}"
    group_data = {"member": [{"name": username}]}

    response = requests.put(
        fortigate_ip + group_endpoint,
        headers=headers,
        data=json.dumps(group_data),
        verify=False,
    )

    if response.status_code == 200 and response.json().get("status") == "success":
        print(f"User '{username}' added to group '{group_name}' successfully.")
    else:
        print(f"Failed to add user '{username}' to group '{group_name}'.")
        print(response.text)


def forti_can_manage_users():
    user_endpoint = "api/v2/cmdb/user/local"
    """Check if the API key has permission to list users, indicating user management access."""
    # url1 = f"https://{fortigate_ip}/api/v2/cmdb/user/local/"
    response = requests.get(fortigate_ip + user_endpoint, headers=headers, verify=False)

    if response.status_code == 200:
        print("API key has permission to manage users.")
        return True
    elif response.status_code == 403:
        print("Permission denied: API key does not have permission to manage users.")
        return False
    else:
        print(
            f"Failed to connect to FortiGate: {response.status_code} - {response.text}"
        )
        return False


def forti_user_exists(username):
    user_endpoint = f"api/v2/cmdb/user/local/{username}"
    """Check if a user with the given username already exists on the FortiGate."""
    # BASE_URL = f"https://{fortigate_ip}"
    # url = f"{BASE_URL}/api/v2/cmdb/user/local/{username}"
    response = requests.get(fortigate_ip + user_endpoint, headers=headers, verify=False)

    if response.status_code == 200:
        print(f"User '{username}' already exists.")
        return True
    elif response.status_code == 404:
        print(f"User '{username}' does not exist and can be created.")
        return False
    else:
        print(
            f"Error checking user existence: {response.status_code} - {response.text}"
        )
        return False


# def modify_forti_user_400f(username, new_group, new_status):
#     new_status=new_status[:-1]
#     """
#     Updates a user's group and status on FortiGate 400F.

#     Args:
#         username (str): The username to update.
#         new_group (str): The new group to assign to the user.
#         new_status (str): The new status for the user ('enable' or 'disable').

#     Returns:
#         dict: Response data from the API.
#     """
#     try:
#         # Step 1: Check if the user exists
#         user_endpoint = f"api/v2/cmdb/user/local/{username}"
#         response = requests.get(fortigate_ip + user_endpoint, headers=headers, verify=False)

#         if response.status_code == 200:
#             print(f"User '{username}' found. Proceeding with update.")
#         else:
#             return {"error": f"User '{username}' not found.", "status_code": response.status_code}

#         # Step 2: Update user's status
#         user_data = response.json()['results'][0]
#         print("******************************")
#         print(f"user_data={user_data}")
#         print("******************************")
#         user_data["status"] = new_status

#         update_response = requests.put(
#             fortigate_ip + user_endpoint, headers=headers, data=json.dumps(user_data), verify=False
#         )

#         if update_response.status_code == 200:
#             print(f"User '{username}' status updated to '{new_status}'.")
#         else:
#             return {
#                 "error": f"Failed to update user status for '{username}'.",
#                 "status_code": update_response.status_code,
#                 "details": update_response.text,
#             }

#         # Step 3: Assign user to the new group
#         group_endpoint = f"api/v2/cmdb/user/group/{new_group}"
#         group_data = {
#             "member": [
#                 {
#                     "name": username
#                 }
#             ]
#         }

#         group_response = requests.put(
#             fortigate_ip + group_endpoint, headers=headers, data=json.dumps(group_data), verify=False
#         )

#         if group_response.status_code == 200:
#             print(f"User '{username}' added to group '{new_group}'.")
#             return {"message": "User updated successfully.", "status_code": 200}
#         else:
#             return {
#                 "error": f"Failed to add user '{username}' to group '{new_group}'.",
#                 "status_code": group_response.status_code,
#                 "details": group_response.text,
#             }

#     except Exception as e:
#         return {"error": str(e)}
