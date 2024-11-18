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

# Set up headers for API key authentication
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_user_400f(user_data):
    user_group = user_data["group"][0]
    print("#############################")
    print(f"user-group is {user_group}")
    print("#############################")

    print("Creating user for a  FortiGate model 400F...")
    # Generic logic for user creation
    user_endpoint = "api/v2/cmdb/user/local"
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
            return True
        else:
            print(f"Failed to add user to group '{user_group}'.")
            print(group_response.text)
            logger.error(
                f"Failed to add user to group '{user_group}' on FortiGate 600D.{group_response.text}"
            )
            return False
    else:
        print("Failed to create user.")
        print(response.text)
        logger.error(f"Failed to create user on FortiGate 600D.{response.text}")
        return False


def modify_forti_user_400f(username, new_group, new_status):
    new_status = new_status[:-1]
    """
    Updates a user's group and status on FortiGate 400F.

    Args:
        username (str): The username to update.
        new_group (str): The new group to assign to the user.
        new_status (str): The new status for the user ('enable' or 'disable').

    Returns:
        dict: Response data from the API.
    """
    try:
        # Step 1: Check if the user exists
        user_endpoint = f"api/v2/cmdb/user/local/{username}"
        response = requests.get(
            fortigate_ip + user_endpoint, headers=headers, verify=False
        )

        if response.status_code != 200:
            return {
                "error": f"User '{username}' not found.",
                "status_code": response.status_code,
            }

        print(f"User '{username}' found. Proceeding with update.")
        user_data = response.json()["results"][0]

        # Step 2: Update user's status
        user_data["status"] = new_status
        update_response = requests.put(
            fortigate_ip + user_endpoint,
            headers=headers,
            data=json.dumps(user_data),
            verify=False,
        )

        if update_response.status_code != 200:
            return {
                "error": f"Failed to update user status for '{username}'.",
                "status_code": update_response.status_code,
                "details": update_response.text,
            }

        print(f"User '{username}' status updated to '{new_status}'.")

        # Step 3: Remove user from all current groups
        group_list_endpoint = "api/v2/cmdb/user/group"
        groups_response = requests.get(
            fortigate_ip + group_list_endpoint, headers=headers, verify=False
        )

        if groups_response.status_code != 200:
            return {
                "error": "Failed to fetch user groups.",
                "status_code": groups_response.status_code,
                "details": groups_response.text,
            }

        group_data = groups_response.json().get("results", [])
        for group in group_data:
            if any(member["name"] == username for member in group.get("member", [])):
                group["member"] = [m for m in group["member"] if m["name"] != username]
                group_update_response = requests.put(
                    fortigate_ip + f"api/v2/cmdb/user/group/{group['name']}",
                    headers=headers,
                    data=json.dumps(group),
                    verify=False,
                )
                if group_update_response.status_code != 200:
                    return {
                        "error": f"Failed to remove user '{username}' from group '{group['name']}'.",
                        "status_code": group_update_response.status_code,
                        "details": group_update_response.text,
                    }

        print(f"User '{username}' removed from all groups.")

        # Step 4: Add user to the new group
        new_group_endpoint = f"api/v2/cmdb/user/group/{new_group}"
        new_group_data = {"member": [{"name": username}]}
        group_response = requests.put(
            fortigate_ip + new_group_endpoint,
            headers=headers,
            data=json.dumps(new_group_data),
            verify=False,
        )

        if group_response.status_code == 200:
            print(f"User '{username}' added to group '{new_group}'.")
            return {"message": "User updated successfully.", "status_code": 200}
        else:
            return {
                "error": f"Failed to add user '{username}' to group '{new_group}'.",
                "status_code": group_response.status_code,
                "details": group_response.text,
            }

    except Exception as e:
        return {"error": str(e)}


def delete_forti_user_400f(username):
    """
    Deletes a user on FortiGate 400F after removing all dependencies.

    Args:
        username (str): The username to delete.

    Returns:
        dict: Response data from the API.
    """
    try:
        # Step 1: Fetch all groups
        group_list_endpoint = "api/v2/cmdb/user/group"
        groups_response = requests.get(
            fortigate_ip + group_list_endpoint, headers=headers, verify=False
        )

        if groups_response.status_code != 200:
            return {
                "error": "Failed to fetch user groups.",
                "status_code": groups_response.status_code,
                "details": groups_response.text,
            }

        groups = groups_response.json().get("results", [])

        # Step 2: Remove user from all groups
        for group in groups:
            if any(member["name"] == username for member in group.get("member", [])):
                group["member"] = [m for m in group["member"] if m["name"] != username]
                group_update_response = requests.put(
                    fortigate_ip + f"api/v2/cmdb/user/group/{group['name']}",
                    headers=headers,
                    data=json.dumps(group),
                    verify=False,
                )
                if group_update_response.status_code != 200:
                    return {
                        "error": f"Failed to remove user '{username}' from group '{group['name']}'.",
                        "status_code": group_update_response.status_code,
                        "details": group_update_response.text,
                    }
                print(f"Removed user '{username}' from group '{group['name']}'.")

        # Step 3: Delete the user
        user_endpoint = f"api/v2/cmdb/user/local/{username}"
        delete_response = requests.delete(
            fortigate_ip + user_endpoint, headers=headers, verify=False
        )

        if delete_response.status_code == 200:
            print(f"User '{username}' deleted successfully.")
            return {
                "message": f"User '{username}' deleted successfully.",
                "status_code": 200,
            }
        else:
            return {
                "error": f"Failed to delete user '{username}'.",
                "status_code": delete_response.status_code,
                "details": delete_response.text,
            }

    except Exception as e:
        return {"error": str(e)}
