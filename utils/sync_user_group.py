import requests
from usrsmgmnt.models import FortiGateUserGroup
from dotenv import load_dotenv
import os
import urllib3

def sync_user_groups():
    # Disable warnings for insecure HTTPS requests
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Load environment variables
    load_dotenv()
    api_key = os.getenv('FORTIGATE_API_KEY')
    fortigate_ip = os.getenv('FORTIGATE_IP')

    # URL for FortiGate API
    fortigate_url = f"https://{fortigate_ip}/api/v2/cmdb/user/group"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        # Send request to FortiGate API to fetch user groups
        response = requests.get(fortigate_url, headers=headers, verify=False)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        user_groups = response.json().get("results", [])

        # Retrieve all existing groups from the database
        existing_groups = {group.name: group for group in FortiGateUserGroup.objects.all()}

        # Add or update groups
        for group in user_groups:
            group_name = group['name']
            if group_name in existing_groups:
                # Update existing group if needed
                existing_groups[group_name].save()  # Add additional field updates if necessary
            else:
                # Add new group
                FortiGateUserGroup.objects.create(name=group_name)

        # Delete groups that are no longer present in FortiGate
        for group_name in list(existing_groups.keys()):
            if group_name not in [group['name'] for group in user_groups]:
                existing_groups[group_name].delete()

        print("User groups synchronized successfully.")
        return true

    except requests.exceptions.RequestException as e:
        print(f"خطا در هنگام بازیابی اطلاعا گروههای کاربری از فایروال {e}")
        return false
    except Exception as e:
        print(f"خطا در هنگام بروزرسانی جدول گروه کاربری {e}")
        return false
