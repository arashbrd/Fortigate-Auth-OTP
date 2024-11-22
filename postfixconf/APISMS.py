import logging
import requests

logging.basicConfig(filename='/var/log/sms/sms.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def sendSMS(phone_num, OTP):
    API_PROVIDER = 'MELLI-PAYAMAK'
    try:
        data = {'bodyId': 213796, 'to': phone_num, 'args': [OTP]}
        response = requests.post('https://console.melipayamak.com/api/send/shared/ae33a10a6bf24822b2dbb101038f5279', json=data)
        return response.json()
    except Exception as e:
        log = f'{e}\n--An error occurred in {API_PROVIDER} for sending SMS'
        return log