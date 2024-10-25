import os
from usrsmgmnt.models import FortiGateUserGroup
import requests
from dotenv import load_dotenv
import urllib3

def update_forti_user_groups(api_url,headers):
    try:
        response = requests.get(api_url, headers=headers, verify=False)
        response.raise_for_status()
        if response.status_code == 200:
            groups = response.json().get("results", [])
            active_ids = [group['id'] for group in groups]  # شناسه‌های فعال از FortiGate

            for group in groups:
                FortiGateUserGroup.objects.update_or_create(
                fortigate_id=group['id'],  # ذخیره شناسه FortiGate در فیلد جداگانه
                defaults={'fortigate_name': group['name']}
                )
            existing_groups = FortiGateUserGroup.objects.all()

            for group in existing_groups:

                if group.fortigate_id not in active_ids:
                    group.delete()
            return True , "به روز رسانی با موفقیت انجام شد"           
            
        else
            return False ,f"Error {response.status_code}: {response.text}"      
       
    except requests.RequestException as e:
        return False ,f"Error fetching groups: {e}"
