import os
import time
import json
import logging
import urllib3
import requests
import core.settings
from dotenv import load_dotenv
from utils.others import utils
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import UserRegistrationForm
from utils.emailProc import process_email
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from utils.sync_user_group import sync_user_groups
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required



logger =  logging.getLogger('db')
# def home(request):
#     return render(request, 'usrsmgmnt/home.html' ,{'show_reg_button': True})

    
def thank_you(request):
    if not request.session.get('from_registration'):
        return redirect('register_user')
    del request.session['from_registration']       
    return render(request, 'usrsmgmnt/thank_you.html',{'show_reg_button': False})

def register_user(request):
    try:    
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            # print('BEFORE FORM VALID*******')
            # print(f'request.POST={request.POST}')
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.last_name.split(' ')[0]+user.national_code[-4:]  
                user.set_password(core.settings.FIX_PASSWORD)
                user.is_active = False 
                user.save()  # ذخیره کاربر
                logger.info(f'کاربر با نام {user.first_name}{user.last_name}به شماره ملی {user.national_code} و شماره موبایل {user.phone_number}در سایت ثبت نام کرد')
                request.session['from_registration'] = True

                #?#TODO:SEND SMS()
                # if send_Sms():
                #     logger.info(f'ارسال شد پیامک برای کاربر "{متن پیامک}"')
                # else:
                #     logger.error(f'پیامک ارسال نشد!!!')
                return redirect('thank_you')  # هدایت به صفحه تشکر
            else:
                errors = form.errors.as_text()
                messages.error(request, errors)
                return render(request, 'usrsmgmnt/register.html', {'form': form,'show_reg_button': False})

        else:
            form = UserRegistrationForm()
        
        return render(request, 'usrsmgmnt/register.html', {'form': form,'show_reg_button': False})
    except Exception as e:
        error_message = str(e)
        if 'UNIQUE constraint' in str(e):
            messages.error(request, 'این ایمیل قبلاً ثبت شده است. لطفاً از ایمیل دیگری استفاده کنید.')
            logger.exception(error_message)

        else:

        # traceback.print_exc()
            messages.error(request, f'خطا: {error_message}')
        return render(request, 'usrsmgmnt/register.html', {'form': form,'show_reg_button': False})
        


@csrf_exempt
def connect_fortigate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Authenticate user locally first
        user = authenticate(request, username=username, password=password)
        if user is not None:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            # time.sleep(5)
            load_dotenv()
            api_key = os.getenv('FORTIGATE_API_KEY')
            fortigate_ip = os.getenv('FORTIGATE_IP')
            # print ("FORTIGATE_IP IS FOUND")
            # print (fortigate_ip)
            fortigate_url = f'https://{fortigate_ip}/api/v2/monitor/system/status'
            

            # Simulated FortiGate connection check with timeout
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }

            try:
                response = requests.get(fortigate_url, headers=headers, verify=False, timeout=5)

                if response.status_code == 200 :
                # and sync_user_groups()
                
                    # FortiGate connection successful
                    # Log in the user if authentication is successful
                    
                    login(request, user)  # This will start the session for the user
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'امکان اتصال به فایروال وجود ندارد'})

            except requests.Timeout:
                return JsonResponse({'success': False, 'message': 'FortiGate connection timed out.'})
            except requests.RequestException as e:
                return JsonResponse({'success': False, 'message': f'Connection error: {str(e)}'})
        else:
            return JsonResponse({'success': False, 'message': 'نام کاربری یا کلمه عبور اشتباه میباشد'})
    return JsonResponse({'success': False, 'message': 'متد ارسال درخواست اشتباه میباشد'})


def home_view(request):
    user_ip = utils.get_client_ip(request)

    logger.info(f'a user visit site with IP:{user_ip}')
    
    return render(request, 'usrsmgmnt/index.html',{'show_reg_button': True})
def download(request):
    return render(request, 'usrsmgmnt/download-software.html',{'show_reg_button': False})
def about_us(request):
    return render(request, 'usrsmgmnt/about-us.html',{'show_reg_button': False})
def education(request):
    return render(request, 'usrsmgmnt/education.html',{'show_reg_button': False})

def steps_page(request):
    
    return render(request, 'usrsmgmnt/steps.html',{'show_reg_button': False})


def run_steps(request):
    try:
        # Simulate step 1
        step1_result = run_step1_script1()[0]
        if not step1_result:
            return JsonResponse({'status': 'fail', 'step': 1, 'error': f'Step 1 failed due to {run_step1_script1()[1]}'})

        # Simulate step 2
        step2_result = run_step2_script()
        if not step2_result:
            return JsonResponse({'status': 'fail', 'step': 2, 'error': 'Step 2 failed due to ...'})

        # Simulate step 3
        step3_result = run_step3_script()
        if not step3_result:
            return JsonResponse({'status': 'fail', 'step': 3, 'error': 'Step 3 failed due to ...'})

        # All steps successful
        return JsonResponse({'status': 'success', 'step': 3})
    
    except Exception as e:
        # Return error if exception occurs
        return JsonResponse({'status': 'fail', 'step': 0, 'error': str(e)})


def run_step1_script1():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()
    api_key = os.getenv('FORTIGATE_API_KEY')
    fortigate_ip = os.getenv('FORTIGATE_IP')
    url = f'https://{fortigate_ip}/api/v2/monitor/system/status'
    headers = {'Authorization': f'Bearer {api_key}'}
    
    response = requests.get(url, headers=headers, verify=False,timeout=5)
    if response.status_code == 200:
        return True ,response.text
    return False ,response.text
def run_step2_script():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()
    api_key = os.getenv('FORTIGATE_API_KEY')
    fortigate_ip = os.getenv('FORTIGATE_IP')
    url = f'https://{fortigate_ip}/api/v2/monitor/system/status'
    headers = {'Authorization': f'Bearer {api_key}'}
    
    response = requests.get(url, headers=headers, verify=False,timeout=5)
    if response.status_code == 200:
        return True
    return False
def run_step3_script():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()
    api_key = os.getenv('FORTIGATE_API_KEY')
    fortigate_ip = os.getenv('FORTIGATE_IP')
    url = f'https://{fortigate_ip}/api/v2/monitor/system/status'
    headers = {'Authorization': f'Bearer {api_key}1'}
    
    response = requests.get(url, headers=headers, verify=False,timeout=5)
    if response.status_code == 200:
        return True
    return False


@staff_member_required
def forti_user_group(request):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()
    api_key = os.getenv('FORTIGATE_API_KEY')
    fortigate_ip = os.getenv('FORTIGATE_IP')
    api_url = f'https://{fortigate_ip}/api/v2/cmdb/user/group'  # Example FortiGate URL for fetching user groups

    headers = {"Authorization": f"Bearer {api_key}"}
    if request.method == 'POST':
        from utils.update_forti_user_groups import update_forti_user_groups
        out,message=update_forti_user_groups(api_url,headers)
        if out:        
            messages.success(request, "به روز رسانی با موفقیت انجام شد")
        else:
             messages.error(request,message )

    return redirect('/admin/')