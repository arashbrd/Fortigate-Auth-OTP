import re
import random



def validate_linux_username(username):
    # Check if the username starts with a lowercase letter
    if not username[0].islower():
        username = 'user_' + username  # Add a default prefix if it starts with an invalid character
    
    # Check if the username contains only valid characters (a-z, 0-9, ., _, -)
    username = re.sub(r'[^a-z0-9._-]', '_', username)  # Replace invalid characters with an underscore
    
    # Ensure the length is within 1 to 32 characters
    username = username[:32]
    
    # List of reserved usernames (system accounts)
    reserved_usernames = ['root', 'admin', 'daemon', 'bin', 'sys', 'sync', 'shutdown', 'halt', 'mail', 'operator']
    
    # Check if the username is reserved, if so, modify it
    if username in reserved_usernames or len(username) == 0:
        username = 'user_' + username
    
    return username

def process_email(email):
    # Extract the username from the email (part before the '@')
    try:
        username = email.split('@')[0]
    except IndexError:
        raise ValueError("Invalid email format")
    
    # Validate the username
    validated_username = validate_linux_username(username)
    
    # If the username is still not valid or has been modified, add a random 3-digit number
    if validated_username != username:
        validated_username += str(random.randint(100, 999))
    
    return validated_username

# Example usage:
# email = input("Enter an email address: ")
# result = process_email(email)
# print(f"The processed username is: {result}")

