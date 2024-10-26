# دیکشنری برای نگهداری توابع با فلگ‌های مشخص
functions = {}

# دکوراتور برای ثبت توابع با فلگ مشخص
def register_retrieve_credit_function(flag):
    def decorator(func):
        functions[flag] = func
        return func
    return decorator

# تعریف توابع با استفاده از دکوراتور
@register_retrieve_credit_function('option1')
def magfa_retrieve_credit(x):
    return x * 2

@register_retrieve_credit_function('option2')
def kavenegar_retrieve_credit(x):
    return x + 10

@register_retrieve_credit_function('option3')
def melli_payamak_retrieve_credit(api_key=api_key):
    '''
    {
  "amount": 37414,
  "status": "شرح خطا در صورت بروز"
    }
    '''
    try:
        api_key=api_key
        response = requests.post('https://console.melipayamak.com/api/receive/credit/{api_key}')
        print(response.json())
    except exceptions as e:
        print(e)



# تابع اصلی برای انتخاب و اجرای تابع براساس فلگ
def retrieve_credit(flag, *args, **kwargs):
    if flag in functions:
        return functions[flag](*args, **kwargs)
    else:
        raise ValueError("Invalid flag value")

# استفاده از تابع اصلی با فلگ مشخص
print(retrieve_credit('option1', 5))  # خروجی: 10
print(retrieve_credit('option2', 5))  # خروجی: 15
print(retrieve_credit('option3', 5))  # خروجی: 25
