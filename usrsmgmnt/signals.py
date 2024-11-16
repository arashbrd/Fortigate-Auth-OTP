from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_login_failed
import logging

logger = logging.getLogger("db")


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # کد مورد نظر خود را اینجا بنویسید
    username = user.username
    ip_address = request.META.get("REMOTE_ADDR", "Unknown IP")

    # Log the failed login attempt
    logger.info(f"Successfull login by: '{username}' from IP '{ip_address}' ")

    # print(f"{user.username} has logged in.")
    # اینجا می‌توانید هر اسکریپت دیگری را اجرا کنید


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    # Get the username attempted (it may or may not be in credentials)
    username = credentials.get("username", "Unknown")
    ip_address = request.META.get("REMOTE_ADDR", "Unknown IP")

    # Log the failed login attempt
    logger.warning(
        f"Failed login attempt for username '{username}' from IP '{ip_address}' "
    )


# signals.py
# import subprocess
# from django.db.models.signals import post_save, post_delete, pre_delete
# from .models import LinFortiUsers
# from django.contrib.auth.models import User
# from .middleware import get_current_request
# from utils.linux.linux_users import create_linux_user
# from django.db import transaction
# from utils.sms.retrieve_credit import check_sms_panel, retrieve_credit
# from utils.linux.linux_users import (
#     create_linux_user,
#     can_create_linux_user,
#     delete_linux_user,
#     update_linux_user,
# )
# from utils.forti.forti_user import (
#     forti_user_exists,
#     forti_can_manage_users,
#     create_forti_user,
#     delete_forti_user,
#     modify_forti_user,
# )
# from core.settings import EMAIL_DOMAIN, MELLI_PAYAMAK_API_KEY
# import datetime
# from utils.sms.send_sms import send_sms
# from django.contrib import messages
# from django.core.exceptions import ValidationError

# from django.utils import timezone
# import traceback

# @receiver(pre_delete, sender=LinFortiUsers)
# def delete_linux_users(sender, instance, **kwargs):
#     print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
#     request = get_current_request()
#     with transaction.atomic():
#         try:
#             # حذف کاربر از لینوکس
#             if delete_linux_user(instance.username):
#                 if delete_forti_user(instance.username):
#                     print("DELETE IS OK")
#                     instance.prevent_delete = False
#                 else:
#                     print("DELETE ERROR IN FORTI")
#                     create_linux_user(
#                     username=instance.username,
#                     first_name=instance.first_name,
#                     last_name=instance.last_name,
#                     phone_number=instance.phone_number
#                 )
#                     instance.prevent_delete = True
#                     messages.error(request, "خطا در حذف کاربر از FortiGate. کاربر لینوکس بازیابی شد.")
#             else:
#                 print("DELETE ERROR IN LINUX")
#                 messages.error(request, "خطا در حذف کاربر از لینوکس.")
#                 instance.prevent_delete = True  # جلوگیری از حذف

#         except Exception as e:
#             print("DELETE ERROR IN EXCEPTION")
#             messages.error(request, f"خطای غیرمنتظره: {str(e)}")
#             instance.prevent_delete = True  # جلوگیری از حذف
#         instance.save(update_fields=['prevent_delete'])

# @receiver(post_save, sender=LinFortiUsers)
# def create_linux_users(sender, instance, created, **kwargs):
#     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

#     request = get_current_request()
#     if not created and request and request.path.startswith('/admin/usrsmgmnt/'):
#         ########################EDITED BY ADMIN
#         usrname=instance.username
#         user_group=instance.user_group.fortigate_name
#         print(f"user_group is {user_group}")
#         phone_number=instance.phone_number
#         is_active=instance.is_active
#         if is_active:
#             status='enable'
#         status='disable'
#         if forti_can_manage_users():
#             if update_linux_user(usrname,phone_number):
#                 if modify_forti_user(status=status,user_group=user_group,username=usrname):
#                     messages.success(request,'اطلاعات فایروال و سرور لینوکس به روز رسانی شدند')
#                 else:
#                     messages.error(request, "خطا در به روز رسانی  کاربر فایروال.--مشخصات کاربر لینوکس و فایروال ممکن است دارای تناقض شده باشد")

#             else:
#                 messages.error(request, "خطا در به روز رسانی  کاربر در لینوکس.")


# @receiver(post_save, sender=LinFortiUsers)
# def create_linux_users(sender, instance, created, **kwargs):
#     request = get_current_request()
#     # print (request.path)
#     try:
#         with transaction.atomic():
#             if created:# INSERT NEW USER
#                 if request and request.path.startswith('/admin/'):
#                     print("INSERT NEW USER VIA ADMIN PANEL")
#                     ########################NEW USER BY ADMIN


#                     usrname=instance.username
#                     password=request.POST.get('password1')
#                     first_name=instance.first_name
#                     last_name=instance.last_name
#                     user_group=instance.user_group.fortigate_name
#                     phone_number=instance.phone_number
#                     is_active=instance.is_active
#                     if is_active:
#                         status='enable'
#                     status='disable'

#                 #     #TODO CHECK USER DOES NOT EXIST
#                     if check_sms_panel(option='option3'):
#                         if can_create_linux_user(usrname):
#                             if forti_can_manage_users() and not forti_user_exists(usrname):
#                                 user_data = {
#                                 "name": usrname,  # Username for the new user
#                                 "passwd": password,  # Set the user's password
#                                 "email-to": usrname+'@'+EMAIL_DOMAIN,  # Email address for two-factor authentication
#                                 "two-factor": "email",  # Enable email-based two-factor authentication
#                                 "status": status,  # User account status: enable or disable
#                                 "group": user_group,  # Add user to the 'edari-access' group
#                                 "auth-concurrent": "disable"  # Disable concurrent authentication
#                                 }
#                                 print ('check_sms_panel is passed #############################')
#                                 if create_linux_user(username=usrname,first_name=first_name,last_name=last_name,phone_number=phone_number):
#                                     print ('create_linux_user is passed #############################')
#                                     if create_forti_user(user_data):
#                                         print ('create_forti_user is passed #############################')

#                                         instance.is_verified=instance.is_active
#                                         if instance.is_verified:
#                                             instance.date_verify=datetime.datetime.now()
#                                         instance.save(update_fields=['is_verified','date_verify'])
#                                         if instance.is_verified:
#                                             pass
#                                             # send_sms('option3',phone_number,264907,MELLI_PAYAMAK_API_KEY,usrname,password)
#                                         print ('send_sms is passed #############################')
#                                     else:
#                                         delete_linux_user(instance.username)
#                                         # raise Exception
#                                         messages.ERROR(request, "در ساخت یوزر در فایروال مشکلی پیش آمده", level=messages.ERROR)

#                                 else:
#                                     #LINUX PROBLEM IN CREATING USER
#                                     print ('create_linux_user NOT passed #############################')
#                                     # raise Exception
#                                     messages.ERROR(request, "در ساخت یوزر در سرور لینوکس مشکلی پیش آمده", level=messages.ERROR)
#                             else:#fORTI
#                                 # fORTI NOT WORKING
#                                 print ('fORTI NOT passed #############################')
#                                 # raise Exception
#                                 messages.ERROR(request, "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد: فایروال ", level=messages.ERROR)
#                         else:#linux
#                             # linux NOT WORKING
#                             print('LINUX NOT passed #############################')
#                             # raise Exception
#                             messages.ERROR(request, "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد:لینوکس  ", level=messages.ERROR)

#                     else:#check_sms_panel
#                         # SMS PANEL NOT WORKING
#                         print ('check_sms_panel NOT passed #############################')
#                         raise ValidationError("در ارتباط با  یکی از موارد زیر مشکلی وجود دارد:پنل پیامکی ")
#                         # messages.ERROR(request, "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد:پنل پیامکی ", level=messages.ERROR)


#                     ########################NEW USER BY ADMIN
#                 else:
#                     print("INSERT NEW USER VIA WEB FORM")
#             else:#EDITED
#                 if request and request.path.startswith('/admin/'):
#                     print("EDITED  USER VIA ADMIN PANEL")
#                     # print(instance.user_group.fortigate_name)


#                 else:
#                     # EDITED VIA WEB FORM
#                     print("HIIII BABY>>>")
#                     pass
#     except Exception as e:
#             # Log the exception or handle it as needed
#             print(f"Error creating  user: {e}")
#             # The transaction will automatically roll back due to the exception
#             raise


# @receiver(pre_delete, sender=LinFortiUsers)
# def delete_linux_users(sender, instance, **kwargs):
#     # request = get_current_request()
#     request = getattr(instance, '_request', None)

#     try:
#         # شروع تراکنش
#         with transaction.atomic():
#             # حذف کاربر از لینوکس
#             if delete_linux_user(instance.username):
#                 # حذف کاربر از FortiGate
#                 if not delete_forti_user(instance.username):
#                     # بازیابی کاربر در لینوکس در صورت خطا
#                     create_linux_user(
#                         username=instance.username,
#                         first_name=instance.first_name,
#                         last_name=instance.last_name,
#                         phone_number=instance.phone_number
#                     )
#                     raise ValidationError("خطا در حذف کاربر از FortiGate. کاربر لینوکس بازیابی شد.")
#             else:
#                 raise ValidationError("خطا در حذف کاربر از لینوکس.")

#     except ValidationError as e:
#         # افزودن پیام خطا به ادمین پنل
#         if request:
#             messages.error(request, str(e))
#         # متوقف کردن حذف رکورد
#         raise e
# @receiver(pre_delete, sender=LinFortiUsers)
# def delete_linux_users(sender, instance, **kwargs):
#     request = get_current_request()
#     try:
#         with transaction.atomic():

#             if delete_linux_user(instance.username):
#                 if delete_forti_user(instance.username):
#                     pass
#                 else:
#                     create_linux_user(username=instance.username,first_name=instance.first_name,last_name=instance.last_name,phone_number=instance.phone_number)
#             else:

#                 raise Exception("در هنگام پاک کردن کاربر لینوکس مشکلی پیش آمده")

#     except Exception as e:
#     # Exception(f"Deletion process failed for user {instance.username}: {str(e)}")
#             messages.error(request, str(e))
#             raise
#             print(f"Error Deleting  user: {e}")
#             # The transaction will automatically roll back due to the exception

# @receiver(post_save, sender=LinFortiUsers)
# def update_linux_user(sender, instance, **kwargs):
#     # Update the Linux user information
#     command = f'sudo usermod -c "{instance.first_name} {instance.last_name}, {instance.national_code}, {instance.phone_number}" {instance.username}'
#     subprocess.run(command, shell=True)
