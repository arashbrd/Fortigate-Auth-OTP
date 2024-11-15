import requests
import logging
from core.settings import MELLI_PAYAMAK_API_KEY
from core.settings import LEAST_CREDIT_NUM


logger =  logging.getLogger('db')
functions = {}
def register_retrieve_credit_function(flag):
    def decorator(func):
        functions[flag] = func
        return func
    return decorator

@register_retrieve_credit_function('option1')
def magfa_retrieve_credit(username,password,domain):
    try:
        contents = requests.get("https://sms.magfa.com/api/http/sms/v1?service=getcredit&username=" + username + "&password=" + password + "&domain=" + 'magfa' + "");
        print(contents.text())
    except Exception as e:
        print(e)


@register_retrieve_credit_function('option2')
def kavenegar_retrieve_credit(x):
    pass

@register_retrieve_credit_function('option3')
def melli_payamak_retrieve_credit():
    '''
    {
  "amount": 37414,
  "status": "شرح خطا در صورت بروز"
    }
    '''
    try:
        
        response = requests.get(f'https://console.melipayamak.com/api/receive/credit/{MELLI_PAYAMAK_API_KEY}')

        
        return response.json()['amount']
    except Exception as e:
        # print (response)
        print(e)
        logger.exception(f'An Exception eccured when fetching credit from SMS panel:{e} ') 
        return response.json()['status']



# تابع اصلی برای انتخاب و اجرای تابع براساس فلگ
def retrieve_credit(flag, *args, **kwargs):
    if flag in functions:
        return functions[flag](*args, **kwargs)
    else:
        raise ValueError("Invalid flag value")

# # استفاده از تابع اصلی با فلگ مشخص
# print(retrieve_credit('option1', 5))  # خروجی: 10
# print(retrieve_credit('option2', 5))  # خروجی: 15
# print(retrieve_credit('option3', 5))  # خروجی: 25



def check_sms_panel(option):
    try:
      
       least_credit_num= int(LEAST_CREDIT_NUM)
       real_credit =int(float(retrieve_credit(option)))
       if real_credit - least_credit_num >0:
           return True
       print(f'amount of panel is {real_credit}')
       return False
    except Exception as e :  
        print(e)      
        logger.exception(f'An Exception eccured when fetching credit from SMS panel:{e} ')    
        return False




