

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
    # captcha = ReCaptchaField(
    #     public_key = '6LcmOGUqAAAAAGh431eYmoup5IFHvUipgHwX6pEX',
    #     private_key = '6LcmOGUqAAAAAOfVCD8LL335UH2_aoMaTilD09q8',
    #     widget=ReCaptchaV3
    #     )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'onkeypress': 'return restrictToEnglish(event)',
            'oninput': 'removeNonEnglish(this)'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'onkeypress': 'return restrictToEnglish(event)',
            'oninput': 'removeNonEnglish(this)'
        })
    )
    class Meta:
        model = LinFortiUsers
        fields = ['first_name', 'last_name','farsi_first_name','farsi_last_name', 'national_code', 'phone_number']
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Regular expression for validating Iranian mobile numbers
        iran_mobile_regex = r'^[0-9]{11}$'

        if not re.match(iran_mobile_regex, phone_number):
            raise ValidationError("فرمت شماره موبایل اشتباه میباشد.مثال 09123456789")

        return phone_number
