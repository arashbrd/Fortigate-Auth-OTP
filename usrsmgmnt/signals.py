# signals.py
import subprocess
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import LinFortiUsers
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in , user_login_failed
import logging
# from django.utils import timezone
logger =  logging.getLogger('db')
@receiver(post_save, sender=LinFortiUsers)
def create_linux_user(sender, instance, created, **kwargs):
    if created:
        # Create a Linux user
        command = f'sudo useradd -m {instance.username} -c "{instance.first_name} {instance.last_name}, {instance.national_code}, {instance.phone_number}"'
        subprocess.run(command, shell=True)

@receiver(post_delete, sender=LinFortiUsers)
def delete_linux_user(sender, instance, **kwargs):
    # Delete the Linux user
    command = f'sudo userdel -r {instance.username}'
    subprocess.run(command, shell=True)

@receiver(post_save, sender=LinFortiUsers)
def update_linux_user(sender, instance, **kwargs):
    # Update the Linux user information
    command = f'sudo usermod -c "{instance.first_name} {instance.last_name}, {instance.national_code}, {instance.phone_number}" {instance.username}'
    subprocess.run(command, shell=True)


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # کد مورد نظر خود را اینجا بنویسید
    username = user.username
    ip_address = request.META.get('REMOTE_ADDR', 'Unknown IP')

    # Log the failed login attempt
    logger.info(
        f"Successfull login by: '{username}' from IP '{ip_address}' "
    )
    
    # print(f"{user.username} has logged in.")
    # اینجا می‌توانید هر اسکریپت دیگری را اجرا کنید




@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    # Get the username attempted (it may or may not be in credentials)
    username = credentials.get('username', 'Unknown')
    ip_address = request.META.get('REMOTE_ADDR', 'Unknown IP')

    # Log the failed login attempt
    logger.warning(
        f"Failed login attempt for username '{username}' from IP '{ip_address}' "
    )
