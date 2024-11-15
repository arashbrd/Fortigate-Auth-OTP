    
import os
import pwd
import subprocess
import logging
logger =  logging.getLogger('db')
add_script_path = os.path.abspath('./utils/linux/scripts/fumsuseradd.sh')

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


def modify_linux_user(username, new_shell=None, new_home=None):
    try:
        cmd = ['sudo', 'usermod']
        
        if new_shell:
            cmd.extend(['-s', new_shell])
        if new_home:
            cmd.extend(['-d', new_home, '-m'])
        
        cmd.append(username)
        subprocess.run(cmd, check=True)
        print(f"User {username} modified successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error modifying user {username}: {e}")



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
       


