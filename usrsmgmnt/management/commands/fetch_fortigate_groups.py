import os
from django.core.management.base import BaseCommand
from usrsmgmnt.models import FortiGateUserGroup
import requests
from dotenv import load_dotenv
import urllib3


class Command(BaseCommand):
    help = 'Fetch user groups from FortiGate and populate FortiGateUserGroup table'
    

    def handle(self, *args, **options):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        load_dotenv()
        api_key = os.getenv('FORTIGATE_API_KEY')
        fortigate_ip = os.getenv('FORTIGATE_IP')
        api_url = f'https://{fortigate_ip}/api/v2/cmdb/user/group'  # Example FortiGate URL for fetching user groups

        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            response = requests.get(api_url, headers=headers, verify=False)
            response.raise_for_status()
            ##+++++++++++
            if response.status_code == 200:
                # Extract the "results" list and retrieve only the "name" field from each entry
                groups = response.json().get("results", [])
                self.stdout.write(self.style.SUCCESS(f'Successful lGroup is: {groups}'))
                # group_names = [group['name'] for group in groups]
                # group_ids = [group['id'] for group in groups]
                active_ids = [group['id'] for group in groups]  # شناسه‌های فعال از FortiGate
                print(f'active_ids[0] Type:{type(active_ids[0])}' )

                self.stdout.write(self.style.SUCCESS(f' active_ids is: {active_ids}'))
                for group in groups:
                    FortiGateUserGroup.objects.update_or_create(
                    fortigate_id=group['id'],  # ذخیره شناسه FortiGate در فیلد جداگانه
                    defaults={'fortigate_name': group['name']}
                    )
                existing_groups = FortiGateUserGroup.objects.all()

                self.stdout.write(self.style.SUCCESS(f'existing_groups  is: {existing_groups}'))

                for group in existing_groups:

                    if group.fortigate_id not in active_ids:
                        print(f'group.fortigate_id in active_ids is:{group.fortigate_id}===>{group.fortigate_id in active_ids}' )
                        print(f'group.fortigate_id Type:{type(group.fortigate_id)}' )
                        group.delete()  # حذف رکورد اگر در FortiGate وجود نداشته باشد

                existing_groups = FortiGateUserGroup.objects.all()
                self.stdout.write(self.style.SUCCESS(f'existing_groups  is: {existing_groups}'))
                
                
                self.stdout.write(self.style.SUCCESS('Successfully updated FortiGateUserGroup table'))
            else:
               self.stdout.write(self.style.ERROR(f"Error {response.status_code}: {response.text}"))
            ##+++++++++++++
            


        
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching groups: {e}"))
