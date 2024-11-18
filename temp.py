import requests
import json
import logging

logger = logging.getLogger("db")
from core.settings import FORTIGATE_API_KEY
from core.settings import FORTIGATE_IP


# FortiGate API details
fortigate_ip = f"https://{FORTIGATE_IP}/"
api_key = f"{FORTIGATE_API_KEY}"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


# Dispatcher function to handle model-specific logic
def create_user(user_data):
    # Fetch FortiGate system details
    model = get_fortigate_model()

    # Dispatch to the appropriate function based on the model
    if model == "400F":
        return create_user_400f(user_data)
    elif model == "600D":

        return create_user_600d(user_data)


# Function to fetch FortiGate model
def get_fortigate_model():
    status_endpoint = "api/v2/monitor/system/status"
    response = requests.get(
        fortigate_ip + status_endpoint, headers=headers, verify=False
    )
    if response.status_code == 200:
        return response.json().get("model", "unknown")
    else:
        raise Exception("Failed to fetch FortiGate model.")


# Specific implementation for FortiGate 400F
def create_user_400f(user_data):
    print("Creating user for FortiGate 400F...")
    # Specific logic for 400F
    user_endpoint = "api/v2/cmdb/user/local/"
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


# Specific implementation for FortiGate 600D


def create_user_600d(user_data):
    user_group = user_data["group"]

    print("Creating user for a generic FortiGate model...")
    # Generic logic for user creation
    user_endpoint = "api/v2/cmdb/user/local/"
    response = requests.post(
        fortigate_ip + user_endpoint,
        headers=headers,
        data=json.dumps(user_data),
        verify=False,
    )

    if response.status_code == 200 and response.json().get("status") == "success":
        print("User created successfully.")

        # Add the user to the group
        group_endpoint = f"api/v2/cmdb/user/group/{user_group}"
        group_data = {"member": [{"name": user_data["name"]}]}

        group_response = requests.put(
            fortigate_ip + group_endpoint,
            headers=headers,
            data=json.dumps(group_data),
            verify=False,
        )

        if (
            group_response.status_code == 200
            and group_response.json().get("status") == "success"
        ):
            print(f"User added to group '{user_group}' successfully.")
        else:
            print(f"Failed to add user to group '{user_group}'.")
            print(group_response.text)
    else:
        print("Failed to create user.")
        print(response.text)


# # Example user data
# user_data = {
#     "name": "2223344",
#     "passwd": "mypass",
#     "email-to": "a@b.com",
#     "two-factor": "email",
#     "status": "enable",
#     "auth-concurrent": "disable"
# }

# # Call the dispatcher function
# create_user(user_data)


# FortiGate API details
# def create_forti_user(user_data):
#     user_group=user_data['group']
# fortigate_ip = "https://192.168.163.1/"
# api_key = "r0m4hgw3jwwHNhn8dfrm916xb7gktr"  # You can also use username and password for login
# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }

# # User data to create
# user_data = {
#     "name": "2223344",
#     "passwd": "mypass",
#     "email-to": "a@b.com",
#     "two-factor": "email",
#     "status": "enabled",
#     "auth-concurrent": "disable"
# }

# # Group data to update
# group_name = "HIS"

# Create the user
# user_endpoint = "api/v2/cmdb/user/local/"
# response = requests.post(fortigate_ip + user_endpoint, headers=headers, data=json.dumps(user_data), verify=False)

# if response.status_code == 200 and response.json().get("status") == "success":
#     print("User created successfully.")

#     # Add the user to the group
#     group_endpoint = f"api/v2/cmdb/user/group/{user_group}"
#     group_data = {
#         "member": [
#             {
#                 "name": user_data["name"]
#             }
#         ]
#     }

#     group_response = requests.put(fortigate_ip + group_endpoint, headers=headers, data=json.dumps(group_data), verify=False)

#     if group_response.status_code == 200 and group_response.json().get("status") == "success":
#         print(f"User added to group '{user_group}' successfully.")
#     else:
#         print(f"Failed to add user to group '{user_group}'.")
#         print(group_response.text)
# else:
#     print("Failed to create user.")
#     print(response.text)
