    
import os
import pwd
import subprocess
import logging
logger =  logging.getLogger('db')
add_script_path = os.path.abspath('./utils/linux/scripts/fumsuseradd.sh')
edit_script_path=os.path.abspath('./utils/linux/scripts/fumsuseredit.sh')
def create_linux_user(**kwargs):
    
    username = kwargs['username']
    full_name = kwargs['first_name'] + " "+kwargs['last_name']
    phone_number=kwargs['phone_number']
    try:
        # Create the user
        result = subprocess.run([add_script_path, username, full_name, phone_number], capture_output=True, text=True)
        
        # Set the password
        if result.returncode == 0:
            logger.info(f'User {username} created successfully in linux server')
            print(f"User {username} created successfully.")
            return True
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating user {username}: {e}")
        print(f"Error creating user {username}: {e}")
        return False


def modify_linux_user(username,phone_number):
    try:
        # Create the user
        result = subprocess.run([edit_script_path, username, phone_number], capture_output=True, text=True)
        
        # Set the password
        if result.returncode == 0:
            logger.info(f'User {username} edited successfully in linux server')
            print(f"User {username} edited successfully.")
            return True
        return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error editing user {username}: {e}")
        print(f"Error editing user {username}: {e}")
        return False


def can_create_linux_user(username):
    # myusername = os.getlogin()
    
    # # Check if running with root privileges
    # if os.geteuid() != 0:
    #     print(f"Permission denied for Current user: {myusername} with userID: {os.geteuid()}: You need to run this script with sudo or as root.")
    #     return False
    
    # Check if username already exists
    try:
        user_info=pwd.getpwnam(username)
        print(f"User '{username}' already exists:{user_info}")
        return False
    except KeyError as e:
        # If KeyError is raised, the user does not exist
        print(f"KeyError is ocurred:{e}")
        pass

    # Optional: Try a dry-run command to confirm useradd command is available
    try:
        
        result = subprocess.run(['sudo', add_script_path, '--help'], capture_output=True, check=True)
        print("User creation command is available.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: useradd command is not available.{e}")
        return False



def delete_linux_user(username):
    try:
        # Run the userdel command with sudo to delete the user
        result = subprocess.run(['sudo', 'userdel', username], capture_output=True, text=True, check=True)
        print(f"User '{username}' deleted successfully.")
        return True
    except subprocess.CalledProcessError as e:
        # Handle the case where the command fails
        # logger.error(f"Error deleting user '{username}':", e.stderr)
        return False
    except TypeError:
        return False
       


import subprocess

def create_linux_user1(username, full_name, phone_number):
    """
    ایجاد یک کاربر جدید در لینوکس بدون دایرکتوری خانگی با جزئیات مشخص شده.

    Args:
        username (str): نام کاربری.
        full_name (str): نام کامل.
        phone_number (str): شماره تلفن.

    Returns:
        str: پیام موفقیت یا خطا.
    """
    try:
        # بررسی وجود کاربر
        check_user = subprocess.run(["id", username], capture_output=True, text=True)
        if check_user.returncode == 0:
            return f"کاربر '{username}' قبلاً ایجاد شده است."

        # دستور برای ایجاد کاربر
        command = [
            "sudo", "useradd",
            "-M",  # جلوگیری از ایجاد دایرکتوری خانگی
            "-s", "/bin/false",  # غیرفعال کردن دسترسی شل
            "-c", f"{full_name},,{phone_number},",  # تنظیم full_name و phone_number
            username  # نام کاربری
        ]

        # اجرای دستور ایجاد کاربر
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return f"کاربر '{username}' با موفقیت ایجاد شد."
        else:
            return f"خطا در ایجاد کاربر: {result.stderr}"

    except Exception as e:
        return f"خطای غیرمنتظره: {str(e)}"
import subprocess

def update_linux_user(username, new_phone_number):
    """
    بروزرسانی شماره تلفن کاربر موجود در لینوکس.

    Args:
        username (str): نام کاربری.
        new_phone_number (str): شماره تلفن جدید.

    Returns:
        str: پیام موفقیت یا خطا.
    """
    try:
        # بررسی وجود کاربر
        check_user = subprocess.run(["id", username], capture_output=True, text=True)
        if check_user.returncode != 0:
            return False

        # گرفتن اطلاعات فعلی کاربر
        get_user_info = subprocess.run(["getent", "passwd", username], capture_output=True, text=True)
        if get_user_info.returncode != 0:
            return False

        # تجزیه اطلاعات فعلی کاربر
        user_info = get_user_info.stdout.strip().split(":")
        current_comment = user_info[4]  # فیلد comment

        # استخراج اطلاعات فعلی
        parts = current_comment.split(",,")
        full_name = parts[0] if len(parts) > 0 else ""
        # تنظیم شماره تلفن جدید
        new_comment = f"{full_name},,{new_phone_number},"

        # دستور برای بروزرسانی اطلاعات کاربر
        command = [
            "sudo", "usermod",
            "-c", new_comment,  # بروزرسانی فیلد comment
            username
        ]

        # اجرای دستور
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False

    except Exception as e:
        return False
