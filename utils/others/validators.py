
import re
from django.core.exceptions import ValidationError


def validate_national_code(value):
    if len(value) != 10 or not value.isdigit():
        raise ValidationError("کد ملی باید شامل 10 رقم باشد.")
    
    # الگوریتم اعتبارسنجی کد ملی
    check = int(value[9])
    s = sum(int(value[x]) * (10 - x) for x in range(9)) % 11
    if not ((s < 2 and check == s) or (s >= 2 and check + s == 11)):
        raise ValidationError("کد ملی نامعتبر است.")

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


def validate_phone_number(value):
    # الگوی معتبر برای شماره موبایل ایران (0 شروع می‌شود و 11 رقم دارد)
    phone_regex = r"^(09)(1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9])\d{7}$"
    
    # چک کردن با استفاده از regex
    if not re.match(phone_regex, value):
        raise ValidationError("شماره موبایل وارد شده معتبر نمی‌باشد. لطفا شماره موبایل ایران را وارد کنید.")
