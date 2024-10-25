# # forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import LinFortiUsers

# class LinFortiUsersCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = LinFortiUsers
#         fields = ('username', 'first_name', 'last_name', 'national_code', 'phone_number','email')
        

# class LinFortiUsersChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = LinFortiUsers
#         fields = ('username', 'first_name', 'last_name', 'national_code', 'phone_number','email')
       


       # usersmgmnt/forms.py
from django import forms
from .models import LinFortiUsers
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3 
import re
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    captcha = ReCaptchaField(
        public_key = '6LcmOGUqAAAAAGh431eYmoup5IFHvUipgHwX6pEX',
        private_key = '6LcmOGUqAAAAAOfVCD8LL335UH2_aoMaTilD09q8',
        widget=ReCaptchaV3
        )
    class Meta:
        model = LinFortiUsers
        fields = ['first_name', 'last_name', 'national_code', 'email', 'phone_number']
        
    # You can add custom validation if needed
    def clean_national_code(self):
        value = self.cleaned_data.get('national_code')
        if not re.match(r'^\d{10}$', value):
            raise ValidationError('کد ملی باید ۱۰ رقم باشد.', params={'value': value})

      # تبدیل کد ملی به لیست از ارقام
        national_code = list(map(int, value))

     # بررسی یکنواخت بودن تمام ارقام (همه ارقام نباید مشابه باشند)
        if all(x == national_code[0] for x in national_code):
            raise ValidationError('کد ملی وارد شده معتبر نیست.', params={'value': value})

    # محاسبه رقم کنترلی
        check = national_code[-1]
        s = sum([national_code[i] * (10 - i) for i in range(9)]) % 11

    # بررسی الگوریتم کنترلی
        if (s < 2 and check != s) or (s >= 2 and check + s != 11):
            raise ValidationError('کد ملی وارد شده معتبر نیست.', params={'value': value})
        return national_code
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Regular expression for validating Iranian mobile numbers
        iran_mobile_regex = r'^09\d{9}$'

        if not re.match(iran_mobile_regex, phone_number):
            raise ValidationError("فرمت شماره موبایل اشتباه میباشد.مثال 09123456789")

        return phone_number
