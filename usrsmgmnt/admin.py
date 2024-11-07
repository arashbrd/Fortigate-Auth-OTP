import logging
from django import forms
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import LinFortiUsers,LogEntry
from django.contrib.auth.models import User
from utils.forti.forti_utils import get_fortigate_specs
from utils.forti.forti_utils import check_all_things_is_ok
from core.settings import DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from utils.sms.retrieve_credit import check_sms_panel,retrieve_credit
from utils.linux.linux_users import create_linux_user,can_create_linux_user
# from django.contrib import messages


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
        sms_panel_credit=retrieve_credit('option3')
        try:
            sms_panel_credit=int(float(sms_panel_credit))
            extra_context['sms_panel'] = sms_panel_credit   # Add the FortiGate specs here
        except Exception as e :
            extra_context['sms_panel'] =sms_panel_credit
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
    def save_model(self, request, obj, form, change):
        # Run the custom script
        if  check_sms_panel(option='option3') and can_create_linux_user(request.user): #TODO  change request.user
            if create_linux_user():
                pass
            else:
                #LINUX PROBLEM IN CREATING USER
                pass

            super().save_model(request, obj, form, change)
            print ("****************CHECK SMS PANEL RUN!!!")
            # messages.success(request, "The record has been saved successfully!!!!")
        else:
            # SMS PANEL NOT WORKING
            pass


    list_display = ('first_name', 'last_name','national_code','email','phone_number','is_active','user_group')
    
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
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email','national_code','phone_number','user_group')}),
        ('وضعیت', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # ('تاریخ‌های مهم', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
    (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'national_code', 'phone_number','email','user_group')
        }
        ),
    )
    

# admin.site.unregister(LinFortiUsers)
admin.site.register(LinFortiUsers, LinFortiUserAdmin)


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('colored_msg', 'create_datetime_format')
    search_fields = ('msg', 'create_datetime')
    list_display_links = ('colored_msg',)
    list_filter = ('level', 'create_datetime')
    list_per_page = DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE

    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = 'green'
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg)

    colored_msg.short_description = 'متن لاگ'

    # def traceback(self, instance):
    #     return format_html('<pre><code>{content}</code></pre>', content=instance.trace if instance.trace else '')

    def create_datetime_format(self, instance):
        return timezone.localtime(instance.create_datetime).strftime('%Y-%m-%d %X')

    create_datetime_format.short_description = 'ایجاد شده در:'
    def has_add_permission(self, request):
        return False

    # اختیاری: غیر فعال کردن دکمه‌های حذف و ویرایش
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(LogEntry, LogEntryAdmin)