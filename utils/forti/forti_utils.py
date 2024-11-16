import os
import requests
import urllib3
from dotenv import load_dotenv


def get_fortigate_specs():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()
    api_key = os.getenv("FORTIGATE_API_KEY")
    fortigate_ip = os.getenv("FORTIGATE_IP")
    url = f"https://{fortigate_ip}/api/v2/monitor/system/status"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.json()
        return {
            "model_name": data.get("results")["model_name"],
            "model": data.get("results")["model"],
            "model_number": data.get("results")["model_number"],
            "firmware_version": data.get("version"),
            "serial": data.get("serial"),
            "hostname": data.get("results")["hostname"],
        }
    return {
        "model": "Not available",
        "firmware_version": "Not available",
        "uptime": "Not available",
        "cpu_usage": "Not available",
        "memory_usage": "Not available",
    }
