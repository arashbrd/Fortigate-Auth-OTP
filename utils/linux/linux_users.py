    
import os
import pwd
import subprocess

def create_linux_user(**kwargs):
    username = kwargs['username']
    password = kwargs['password']
    try:
        # Create the user
        subprocess.run(['sudo', 'useradd', '-m', '-s', '/bin/bash', username], check=True)
        
        # Set the password
        subprocess.run(['echo', f'{username}:{password}', '|', 'sudo', 'chpasswd'], shell=True, check=True)
        print(f"User {username} created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user {username}: {e}")


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

def delete_linux_user(username):
    try:
        subprocess.run(['sudo', 'userdel', '-r', username], check=True)
        print(f"User {username} deleted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting user {username}: {e}")


def can_create_linux_user(username):
    # Check if running with root privileges
    if os.geteuid() != 0:
        print("Permission denied: You need to run this script with sudo or as root.")
        return False
    
    # Check if username already exists
    try:
        pwd.getpwnam(username)
        print(f"User '{username}' already exists.")
        return False
    except KeyError:
        # If KeyError is raised, the user does not exist
        pass

    # Optional: Try a dry-run command to confirm useradd command is available
    try:
        result = subprocess.run(['sudo', 'useradd', '--help'], capture_output=True, check=True)
        print("User creation command is available.")
        return True
    except subprocess.CalledProcessError:
        print("Error: useradd command is not available.")
        return False


