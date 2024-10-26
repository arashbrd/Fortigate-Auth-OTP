import requests
# دیکشنری برای نگهداری توابع با فلگ‌های مشخص
functions = {}

# دکوراتور برای ثبت توابع با فلگ مشخص
def register_send_sms_function(flag):
    def decorator(func):
        functions[flag] = func
        return func
    return decorator

# تعریف توابع با استفاده از دکوراتور
@register_send_sms_function('option1')
def magfa_send_sms(x):
    return x * 2

@register_send_sms_function('option2')
def kavenegar_send_sms(x):
    return x + 10

@register_send_sms_function('option3')
def melli_payamak_send_sms(to,bodyId=bodyId,arg1=arg1,arg2=arg2,api_key=api_key):
    '''
    { 
    "bodyId": 524, 
    "to": "09123456789", 
    "args": ["arg1", "arg2"]
    }
    {
    "recId": 3741437414,
    "status": "شرح خطا در صورت بروز"
    }
    '''
    try:
        data = {'bodyId': bodyId, 'to': to , 'args': [arg1, arg2]}
        api_key=api_key
        response = requests.post('https://console.melipayamak.com/api/send/shared/{api_key}', json=data)
        print(response.json())
    except exceptions as e:
        print(e)


# تابع اصلی برای انتخاب و اجرای تابع براساس فلگ
def send_sms(flag, *args, **kwargs):
    if flag in functions:
        return functions[flag](*args, **kwargs)
    else:
        raise ValueError("Invalid flag value")

# استفاده از تابع اصلی با فلگ مشخص
print(send_sms('option1', 5))  # خروجی: 10
print(send_sms('option2', 5))  # خروجی: 15
print(send_sms('option3', 5))  # خروجی: 25
