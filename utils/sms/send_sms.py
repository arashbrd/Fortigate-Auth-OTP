import requests
functions = {}

def register_send_sms_function(flag):
    def decorator(func):
        functions[flag] = func
        return func
    return decorator

# @register_send_sms_function('option1')
# def magfa_send_sms(username,password,to,from,text,domain):
        
#     return  requests.get('https://sms.magfa.com/api/http/sms/v1?service=enqueue&username={username}&password={password}&domain={domain}&from={from}&to={to}&text={text}');

    

@register_send_sms_function('option2')
def kavenegar_send_sms(x):
    return x + 10

@register_send_sms_function('option3')
def melli_payamak_send_sms(to,bodyId,api_key,*args):
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
        data = {'to':to ,'bodyId': bodyId, 'args': args}   
        print (f'to={to}')    
        print (f'bodyId={bodyId}')    
        print (f'api_key={api_key}')    
        print (f'args={args}')    
          
        
        response = requests.post(f'https://console.melipayamak.com/api/send/shared/{api_key}', json=data)
        print(response.json())
    except Exception as e:
        print(e)


def send_sms(flag, *args, **kwargs):
    if flag in functions:
        return functions[flag](*args, **kwargs)
    else:
        raise ValueError("Invalid flag value")

# print(send_sms('option1', 5))  # خروجی: 10
# print(send_sms('option2', 5))  # خروجی: 15
# print(send_sms('option3', 5))  # خروجی: 25

# if __name__ == "__main__":
#     send_sms('option3','09173303491',264902,'ae33a10a6bf24822b2dbb101038f5279','آرش بردبار')