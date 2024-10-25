import os
import requests
import urllib3
from dotenv import load_dotenv
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import Group
from .models import LinFortiUsers
# from django.contrib import messages
from django import forms


# Function to fetch FortiGate specs
def get_fortigate_specs():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()
    api_key = os.getenv('FORTIGATE_API_KEY')
    fortigate_ip = os.getenv('FORTIGATE_IP')
    url = f'https://{fortigate_ip}/api/v2/monitor/system/status'
    headers = {'Authorization': f'Bearer {api_key}'}
    
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.json()
        return {
            'model_name': data.get('results')['model_name'],
            'model': data.get('results')['model'],
            'model_number': data.get('results')['model_number'],
            'firmware_version': data.get('version'),
            'serial': data.get('serial'),
            'hostname': data.get('results')['hostname'],
            
        }
    return {'model':'Not available',
            'firmware_version': 'Not available',
            'uptime': 'Not available',
            'cpu_usage':'Not available',
            'memory_usage':'Not available',}

# Custom admin site class
class CustomAdminSite(admin.AdminSite):
    site_header = "پنل مدیریت کاربران احراز هویت دو مرحله ای"
    site_title = "کاربران"
    index_title = "خوش آمدید"

    def index(self, request, extra_context=None):
        # messages.info(request, "در حال اتصال و به‌روزرسانی داده‌ها...")
        # print("Index function called")
        extra_context = extra_context or {}
        extra_context['fortigate_specs'] = get_fortigate_specs()  # Add the FortiGate specs here
        return super().index(request, extra_context=extra_context)

# Instantiate your custom admin site
admin_site = CustomAdminSite()

admin.site = admin_site




class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # پنهان کردن بخش permissions
        if 'user_permissions' in self.fields:
            self.fields['user_permissions'].widget = forms.HiddenInput()

class LinFortiUserAdmin(BaseUserAdmin):
    list_display = ('first_name', 'last_name','national_code','email','phone_number','is_active')
    
    # قابلیت جستجو در این فیلدها
    search_fields = ('username', 'email', 'first_name', 'last_name','phone_number')

    # قابلیت فیلتر بر اساس این فیلدها
    list_filter = ('is_staff', 'is_active')

    # قابلیت تغییر چند کاربر به صورت همزمان
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "کاربران انتخاب شده فعال شدند.")

    activate_users.short_description = "فعال کردن کاربران انتخاب شده"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "کاربران انتخاب شده غیرفعال شدند.")

    deactivate_users.short_description = "غیرفعال کردن کاربران انتخاب شده"

    form = CustomUserChangeForm

    # حذف بخش permissions از فرم ادمین
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email','phone_number')}),
        ('وضعیت', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # ('تاریخ‌های مهم', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
    (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'national_code', 'phone_number','email')
        }
        ),
    )
    

# admin.site.unregister(LinFortiUsers)
admin.site.register(LinFortiUsers, LinFortiUserAdmin)
