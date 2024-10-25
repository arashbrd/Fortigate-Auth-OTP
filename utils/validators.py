
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_national_code(value):
    # بررسی طول و الگوی کد ملی (باید ۱۰ رقم باشد)
    if not re.match(r'^\d{10}$', value):
        raise ValidationError(_('کد ملی باید ۱۰ رقم باشد.'), params={'value': value})

    # تبدیل کد ملی به لیست از ارقام
    national_code = list(map(int, value))

    # بررسی یکنواخت بودن تمام ارقام (همه ارقام نباید مشابه باشند)
    if all(x == national_code[0] for x in national_code):
        raise ValidationError(_('کد ملی وارد شده معتبر نیست.'), params={'value': value})

    # محاسبه رقم کنترلی
    check = national_code[-1]
    s = sum([national_code[i] * (10 - i) for i in range(9)]) % 11

    # بررسی الگوریتم کنترلی
    if (s < 2 and check != s) or (s >= 2 and check + s != 11):
        raise ValidationError(_('کد ملی وارد شده معتبر نیست.'), params={'value': value})


def validate_linux_username(username):
    # Check length (1 to 32 characters)
    if not (1 <= len(username) <= 32):
        raise ValidationError("Username must be between 1 and 32 characters long.")
    
    # Check if the username starts with a lowercase letter
    if not username[0].islower():
        raise ValidationError("Username must start with a lowercase letter.")
    
    # Check if the username contains only valid characters (a-z, 0-9, ., _, -)
    if not re.match(r'^[a-z][a-z0-9._-]*$', username):
        raise ValidationError("Username can only contain lowercase letters, numbers, '.', '_', and '-'.")
    
    # List of reserved usernames (system accounts)
    reserved_usernames = ['root', 'admin', 'daemon', 'bin', 'sys', 'sync', 'shutdown', 'halt', 'mail', 'operator']
    
    # Check if the username is not in the reserved usernames list
    if username in reserved_usernames:
        raise ValidationError(f"The username '{username}' is reserved and cannot be used.")
