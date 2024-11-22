import sys
import subprocess
import logging
from APISMS import sendSMS

email = sys.argv[1]
OTP = sys.argv[2]

logging.basicConfig(filename='/var/log/sms/sms.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_username(email):
    parts = email.split('@')
    return parts[0] if len(parts) == 2 else None

def get_work_phone(username):
    try:
        result = subprocess.run(['grep', f'^{username}:', '/etc/passwd'], capture_output=True, text=True, check=True)
        user_info = result.stdout.strip().split(':')[4]
        work_phone = user_info.split(',')[2]
        return work_phone, user_info.split(',')[0]
    except subprocess.CalledProcessError:
        logging.error('User not found or an error occurred')
        return None, 'No full name exists'

def main():
    if len(sys.argv) != 3:
        logging.error("Usage: Should supply email and OTP")
        return

    username = extract_username(email)
    phone_num, fullname = get_work_phone(username)
    if phone_num and username:
        log = sendSMS(phone_num, OTP)
        if isinstance(log, dict):
            logging.info(log)
        else:
            logging.error(log)
    else:
        logging.error(f"No phone number or username found for {fullname}")

if __name__ == "__main__":
    main()