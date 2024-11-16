import logging
from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from utils.sms.send_sms import send_sms
from django.utils.html import format_html
from .models import LinFortiUsers, LogEntry

from utils.forti.forti_utils import get_fortigate_specs
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from utils.sms.retrieve_credit import check_sms_panel, retrieve_credit
from utils.linux.linux_users import (
    create_linux_user,
    can_create_linux_user,
    delete_linux_user,
    update_linux_user,
)
from utils.forti.forti_user import (
    forti_user_exists,
    forti_can_manage_users,
    create_forti_user,
    delete_forti_user,
    modify_forti_user,
)
from core.settings import (
    DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE,
    EMAIL_DOMAIN,
    MELLI_PAYAMAK_API_KEY,
)
import datetime
from .forms import CustomUserChangeForm
from django.db import transaction


# Custom admin site class
class CustomAdminSite(admin.AdminSite):

    site_header = "پنل مدیریت کاربران احراز هویت دو مرحله ای"
    site_title = "کاربران"
    index_title = "خوش آمدید"

    def index(self, request, extra_context=None):
        # messages.info(request, "در حال اتصال و به‌روزرسانی داده‌ها...")
        # print("Index function called")
        extra_context = extra_context or {}
        extra_context["fortigate_specs"] = (
            get_fortigate_specs()
        )  # Add the FortiGate specs here
        sms_panel_credit = retrieve_credit("option3")
        try:
            sms_panel_credit = int(float(sms_panel_credit))
            extra_context["sms_panel"] = (
                sms_panel_credit  # Add the FortiGate specs here
            )
        except Exception:
            extra_context["sms_panel"] = sms_panel_credit
        return super().index(request, extra_context=extra_context)


# Instantiate your custom admin site
admin_site = CustomAdminSite()

admin.site = admin_site


class LinFortiUserAdmin(BaseUserAdmin):
    def message_user(
        self,
        request,
        message,
        level=messages.SUCCESS,
        extra_tags="",
        fail_silently=False,
    ):
        """
        بازنویسی متد message_user برای جلوگیری از پیام پیش‌فرض حذف
        """
        if "حذف شد" not in message:  # جلوگیری از پیام پیش‌فرض حذف
            super().message_user(request, message, level, extra_tags, fail_silently)
        if " تغییر " in message:  # جلوگیری از پیام پیش‌فرض حذف
            return

    def delete_model(self, request, obj):
        total_deleted = 0
        with transaction.atomic():
            try:
                if delete_linux_user(obj.username):
                    if delete_forti_user(obj.username):
                        print("DELETE IS OK")
                        obj.prevent_delete = False

                    else:
                        print("DELETE ERROR IN FORTI")
                        create_linux_user(
                            username=obj.username,
                            first_name=obj.first_name,
                            last_name=obj.last_name,
                            phone_number=obj.phone_number,
                        )
                        obj.prevent_delete = True
                        messages.error(
                            request,
                            "خطا در حذف کاربر از FortiGate. کاربر لینوکس بازیابی شد.",
                        )
                else:
                    print("DELETE ERROR IN LINUX")
                    messages.error(request, "خطا در حذف کاربر از لینوکس.")
                    obj.prevent_delete = True  # جلوگیری از حذف

            except Exception as e:
                print("DELETE ERROR IN EXCEPTION")
                messages.error(request, f"خطای غیرمنتظره: {str(e)}")
                obj.prevent_delete = True  # جلوگیری از حذف
            obj.save(update_fields=["prevent_delete"])

            if not obj.prevent_delete:
                obj.delete()
                print("**********************")
                total_deleted += 1
                print(f"total_deleted ={total_deleted}")
                self.message_user(
                    request, "یک کاربر با موفقیت پاک شد.", level=messages.SUCCESS
                )
            else:
                # self.message_user(request, f"خطا",level=messages.ERROR)
                pass
        # if total_deleted == 1:

        #     self.message_user(request, "یک کاربر با موفقیت پاک شد.", level=messages.SUCCESS)
        # elif total_deleted > 1:
        #     self.message_user(request, f"{total_deleted} کاربر با موفقیت پاک شدند.", level=messages.SUCCESS)
        # else:
        #     self.message_user(request, "هیچ کاربری پاک نشد.", level=messages.WARNING)

    def delete_queryset(self, request, queryset):
        total_deleted = 0
        with transaction.atomic():
            for obj in queryset:
                try:
                    if delete_linux_user(obj.username):
                        if delete_forti_user(obj.username):
                            print("DELETE IS OK")
                            obj.prevent_delete = False
                        else:
                            print("DELETE ERROR IN FORTI")
                            create_linux_user(
                                username=obj.username,
                                first_name=obj.first_name,
                                last_name=obj.last_name,
                                phone_number=obj.phone_number,
                            )
                            obj.prevent_delete = True
                            messages.error(
                                request,
                                "خطا در حذف کاربر از FortiGate. کاربر لینوکس بازیابی شد.",
                            )
                    else:
                        print("DELETE ERROR IN LINUX")
                        messages.error(request, "خطا در حذف کاربر از لینوکس.")
                        obj.prevent_delete = True  # جلوگیری از حذف
                except Exception as e:
                    print("DELETE ERROR IN EXCEPTION")
                    messages.error(request, f"خطای غیرمنتظره: {str(e)}")
                    obj.prevent_delete = True  # جلوگیری از حذف
                obj.save(update_fields=["prevent_delete"])

                print("**********************")
                print(f"obj.prevent_delete ={obj.prevent_delete}")
                if not obj.prevent_delete:
                    obj.delete()
                    print("**********************")
                    total_deleted += 1
                    print(f"total_deleted ={total_deleted}")
                else:
                    # self.message_user(request, f"خطا",level=messages.ERROR)
                    pass
            if total_deleted == 1:

                self.message_user(
                    request, "یک کاربر با موفقیت پاک شد.", level=messages.SUCCESS
                )
            elif total_deleted > 1:
                self.message_user(
                    request,
                    f"{total_deleted} کاربر با موفقیت پاک شدند.",
                    level=messages.SUCCESS,
                )
            else:
                self.message_user(
                    request, "هیچ کاربری حذف نشد.", level=messages.WARNING
                )

    # add_form = CustomUserChangeForm
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)

    #     # ارسال متغیر به قالب تنها در حالت افزودن
    #     if obj is None:  # اگر obj وجود ندارد، یعنی در حالت افزودن هستیم
    #         self.is_in_add_form = True
    #     else:
    #         self.is_in_add_form = False
    #     return form

    # def render_change_form(self, request, context, *args, **kwargs):
    #     # اضافه کردن متغیر به کانتکست
    #     context['is_in_add_form'] = getattr(self, 'is_in_add_form', False)
    #     return super().render_change_form(request, context, *args, **kwargs)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        obj = self.get_object(request, object_id)
        extra_context = extra_context or {}
        # اگر مقدار status در دیتابیس ۱ بود، به قالب ارسال کنید
        extra_context["is_verified"] = obj.is_verified if obj else False
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def save_model(self, request, obj, form, change):
        # req = get_current_request()
        print(f"change is {change}")
        if change:
            if request and request.path.startswith("/admin/usrsmgmnt/"):
                if obj.is_verified:
                    print("CHANGE IS TRUE")
                    # EDIT USER BY REGISTERATION IN ADMIN PANEL
                    # ********************************
                    # obj.user_group=[form.cleaned_data.get('user_group').fortigate_name]
                    usrname = obj.username
                    user_group = form.cleaned_data.get("user_group").fortigate_name
                    phone_number = request.POST.get("phone_number")
                    print(f"user_group is {user_group}")
                    user_group_id = request.POST.get("user_group")
                    if user_group_id:
                        try:
                            # اگر user_group یک ForeignKey است، مقدار را به شیء مرتبط تبدیل کنید
                            from .models import FortiGateUserGroup  # مدل مرتبط

                            obj.user_group = FortiGateUserGroup.objects.get(
                                pk=user_group_id
                            )
                        except FortiGateUserGroup.DoesNotExist:
                            obj.user_group = None  # مقدار نامعتبر: فیلد را خالی بگذارید
                    else:
                        obj.user_group = None

                    is_active = request.POST.get("is_active")
                    if is_active == "on":
                        is_active = True
                        status = "enable"
                    else:
                        is_active = False
                        status = "disable"
                    is_superuser = request.POST.get("is_superuser")
                    if is_superuser == "on":
                        is_superuser = True
                    else:
                        is_superuser = False
                    is_staff = request.POST.get("is_staff")
                    if is_staff == "on":
                        is_staff = True
                    else:
                        is_staff = False
                    obj.phone_number = request.POST.get("phone_number")
                    obj.is_active = is_active
                    obj.is_superuser = is_superuser
                    obj.is_staff = is_staff
                    if check_sms_panel(option="option3"):
                        if forti_can_manage_users():
                            if update_linux_user(usrname, phone_number):
                                if modify_forti_user(
                                    status=status,
                                    user_group=user_group,
                                    username=usrname,
                                ):
                                    obj.save(
                                        update_fields=[
                                            "user_group",
                                            "phone_number",
                                            "is_active",
                                            "is_superuser",
                                            "is_staff",
                                        ]
                                    )
                                    # send_sms('option3',phone_number,264907,MELLI_PAYAMAK_API_KEY,usrname,obj.password)

                                    messages.success(
                                        request,
                                        "اطلاعات فایروال و سرور لینوکس به روز رسانی شدند",
                                    )
                                else:
                                    messages.error(
                                        request,
                                        "خطا در به روز رسانی  کاربر فایروال.--مشخصات کاربر لینوکس و فایروال ممکن است دارای تناقض شده باشد",
                                    )

                            else:
                                messages.error(
                                    request, "خطا در به روز رسانی  کاربر در لینوکس."
                                )
                        else:
                            messages.error(request, "خطا در  دسترسی به فایروال.")

                    else:
                        # SMS PANEL NOT WORKING
                        print(
                            "check_sms_panel NOT passed #############################"
                        )
                        self.message_user(
                            request,
                            "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد:پنل پیامکی ",
                            level=messages.ERROR,
                        )
                        # ************************************

                    # if not obj.is_verified and obj.is_active:
                    #     obj.is_verified=obj.is_active
                    #     obj.date_verify=datetime.datetime.now()

                    # EDIT USER BY REGISTERATION IN ADMIN PANEL
                    # ************************************
                else:
                    # obj.is_verified is not TRUE and Admin should verify user
                    # ************************************
                    usrname = request.POST.get("username")
                    password = request.POST.get("password1")
                    first_name = request.POST.get("first_name")
                    last_name = request.POST.get("last_name")
                    user_group = [form.cleaned_data.get("user_group").fortigate_name]
                    phone_number = request.POST.get("phone_number")
                    is_active = request.POST.get("is_active")
                    if is_active:
                        status = "enable"
                    status = "disable"
                    if check_sms_panel(option="option3"):
                        if can_create_linux_user(usrname):
                            if forti_can_manage_users() and not forti_user_exists(
                                usrname
                            ):
                                obj.is_verified = True
                                obj.date_verify = datetime.datetime.now()
                                user_data = {
                                    "name": usrname,  # Username for the new user
                                    "passwd": password,  # Set the user's password
                                    "email-to": usrname
                                    + "@"
                                    + EMAIL_DOMAIN,  # Email address for two-factor authentication
                                    "two-factor": "email",  # Enable email-based two-factor authentication
                                    "status": status,  # User account status: enable or disable
                                    "group": user_group,  # Add user to the 'edari-access' group
                                    "auth-concurrent": "disable",  # Disable concurrent authentication
                                }
                                print(
                                    "check_sms_panel is passed #############################"
                                )
                                if create_linux_user(
                                    username=usrname,
                                    first_name=first_name,
                                    last_name=last_name,
                                    phone_number=phone_number,
                                ):
                                    print(
                                        "create_linux_user is passed #############################"
                                    )
                                    if create_forti_user(user_data):
                                        print(
                                            "create_forti_user is passed #############################"
                                        )
                                        super().save_model(request, obj, form, change)
                                        # send_sms('option3',phone_number,264907,MELLI_PAYAMAK_API_KEY,usrname,password)
                                    else:
                                        delete_linux_user(usrname)
                                        self.message_user(
                                            request,
                                            "در ساخت یوزر در فایروال مشکلی پیش آمده",
                                            level=messages.ERROR,
                                        )

                                else:
                                    # LINUX PROBLEM IN CREATING USER
                                    print(
                                        "create_linux_user NOT passed #############################"
                                    )
                                    self.message_user(
                                        request,
                                        "در ساخت یوزر در سرور لینوکس مشکلی پیش آمده",
                                        level=messages.ERROR,
                                    )
                            else:  # fORTI
                                # fORTI NOT WORKING
                                print("fORTI NOT passed #############################")
                                self.message_user(
                                    request,
                                    "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد: فایروال ",
                                    level=messages.ERROR,
                                )
                        else:  # linux
                            # linux NOT WORKING
                            print("LINUX NOT passed #############################")
                            self.message_user(
                                request,
                                "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد:لینوکس  ",
                                level=messages.ERROR,
                            )
                    else:
                        # SMS PANEL NOT WORKING
                        print(
                            "check_sms_panel NOT passed #############################"
                        )
                        self.message_user(
                            request,
                            "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد:پنل پیامکی ",
                            level=messages.ERROR,
                        )
                        # ************************************
            else:
                # EDIT USER BY REGISTERATION IN WEBFORM
                # ********************************

                pass

                # ************************************

        else:
            # NEW USER BY REGISTERATION IN ADMIN PANEL
            # ********************************

            if request and request.path.startswith("/admin/usrsmgmnt/"):

                print(" CHANGE IS TRUE NEW USER....")
                # ADD NEW USER BY ADMIN
                # ********************************
                usrname = request.POST.get("username")
                password = request.POST.get("password1")
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")
                user_group = [form.cleaned_data.get("user_group").fortigate_name]
                phone_number = request.POST.get("phone_number")
                is_active = request.POST.get("is_active")
                if is_active:
                    status = "enable"
                status = "disable"
                # TODO CHECK USER DOES NOT EXIST
                if check_sms_panel(option="option3"):
                    if can_create_linux_user(usrname):
                        if forti_can_manage_users() and not forti_user_exists(usrname):
                            user_data = {
                                "name": usrname,  # Username for the new user
                                "passwd": password,  # Set the user's password
                                "email-to": usrname
                                + "@"
                                + EMAIL_DOMAIN,  # Email address for two-factor authentication
                                "two-factor": "email",  # Enable email-based two-factor authentication
                                "status": status,  # User account status: enable or disable
                                "group": user_group,  # Add user to the 'edari-access' group
                                "auth-concurrent": "disable",  # Disable concurrent authentication
                            }
                            print(
                                "check_sms_panel is passed #############################"
                            )
                            if create_linux_user(
                                username=usrname,
                                first_name=first_name,
                                last_name=last_name,
                                phone_number=phone_number,
                            ):
                                print(
                                    "create_linux_user is passed #############################"
                                )
                                if create_forti_user(user_data):
                                    print(
                                        "create_forti_user is passed #############################"
                                    )

                                    obj.is_verified = obj.is_active
                                    if obj.is_verified:
                                        obj.date_verify = datetime.datetime.now()

                                    super().save_model(request, obj, form, change)
                                    print(
                                        "save model is passed #############################"
                                    )
                                    if obj.is_verified:
                                        pass
                                        # send_sms('option3',phone_number,264907,MELLI_PAYAMAK_API_KEY,usrname,password)

                                    print(
                                        "send_sms is passed #############################"
                                    )
                                else:
                                    delete_linux_user(usrname)
                                    self.message_user(
                                        request,
                                        "در ساخت یوزر در فایروال مشکلی پیش آمده",
                                        level=messages.ERROR,
                                    )

                            else:
                                # LINUX PROBLEM IN CREATING USER
                                print(
                                    "create_linux_user NOT passed #############################"
                                )
                                self.message_user(
                                    request,
                                    "در ساخت یوزر در سرور لینوکس مشکلی پیش آمده",
                                    level=messages.ERROR,
                                )
                        else:  # fORTI
                            # fORTI NOT WORKING
                            print("fORTI NOT passed #############################")
                            self.message_user(
                                request,
                                "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد: فایروال ",
                                level=messages.ERROR,
                            )
                    else:  # linux
                        # linux NOT WORKING
                        print("LINUX NOT passed #############################")
                        self.message_user(
                            request,
                            "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد:لینوکس  ",
                            level=messages.ERROR,
                        )

                else:  # check_sms_panel
                    # SMS PANEL NOT WORKING
                    print("check_sms_panel NOT passed #############################")
                    self.message_user(
                        request,
                        "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد:پنل پیامکی ",
                        level=messages.ERROR,
                    )
                    # ************************************

            else:
                print(" CHANGE IS FALSE... NEW USER BY WEB FORM....")
                # ADD NEW USER BY WEB FORM
                # ********************************
                pass

                # ********************************

    # def save_my_model(self, request, obj, form, change):
    #     print ('1#############################')
    #     usrname=request.POST.get('username')
    #     password=request.POST.get('national_code')[-4:]
    #     first_name=request.POST.get('first_name')
    #     last_name=request.POST.get('last_name')
    #     user_group=[form.cleaned_data.get('user_group').fortigate_name]
    #     phone_number=request.POST.get('phone_number')

    #     if user_group!=['']:
    #         print ('not changed #############################')
    #         if  check_sms_panel(option='option3'):
    #             if can_create_linux_user(usrname):
    #                 if forti_can_manage_users() and not forti_user_exists(usrname): #TODO  change request.user
    #                     user_data = {
    #                     "name": usrname,  # Username for the new user
    #                     "passwd": password,  # Set the user's password
    #                     "email-to": usrname+'@'+EMAIL_DOMAIN,  # Email address for two-factor authentication
    #                     "two-factor": "email",  # Enable email-based two-factor authentication
    #                     "status": "enable",  # User account status: enable or disable
    #                     "group": user_group,  # Add user to the 'edari-access' group
    #                     "auth-concurrent": "disable"  # Disable concurrent authentication
    #                     }
    #                     print ('check_sms_panel is passed #############################')
    #                     if create_linux_user(username=usrname,first_name=first_name,last_name=last_name,phone_number=phone_number):
    #                         print ('create_linux_user is passed #############################')
    #                         if create_forti_user(user_data):
    #                             print ('create_forti_user is passed #############################')

    #                             obj.is_verified=True
    #                             obj.date_verify=datetime.datetime.now()
    #                             super().save_model(request, obj, form, change)
    #                             print ('save model is passed #############################')
    #                             # send_sms('option3',phone_number,264907,MELLI_PAYAMAK_API_KEY,usrname,password)
    #                             print ('send_sms is passed #############################')
    #                         else:
    #                             delete_linux_user(usrname)
    #                             self.message_user(request, "در ساخت یوزر در فایروال مشکلی پیش آمده", level=messages.ERROR)

    #                     else:
    #                         #LINUX PROBLEM IN CREATING USER
    #                         print ('create_linux_user NOT passed #############################')
    #                         self.message_user(request, "در ساخت یوزر در سرور لینوکس مشکلی پیش آمده", level=messages.ERROR)
    #                 else:#fORTI
    #                     # fORTI NOT WORKING
    #                     print ('fORTI NOT passed #############################')
    #                     self.message_user(request, "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد: فایروال ", level=messages.ERROR)
    #             else:#linux
    #                 # linux NOT WORKING
    #                 print ('LINUX NOT passed #############################')
    #                 self.message_user(request, "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد:لینوکس  ", level=messages.ERROR)

    #         else:#check_sms_panel
    #             # SMS PANEL NOT WORKING
    #             print ('check_sms_panel NOT passed #############################')
    #             self.message_user(request, "در ارتباط با  یکی از موارد زیر مشکلی وجود دارد:پنل پیامکی ", level=messages.ERROR)

    #     else:#user_group
    #         print ('CHANGE IS TRUE #############################')
    #         self.message_user(request, "Script failed, object was not saved.", level=messages.ERROR)

    list_display = (
        "farsi_first_name",
        "farsi_last_name",
        "first_name",
        "last_name",
        "national_code",
        "phone_number",
        "is_active",
        "user_group",
    )

    # قابلیت جستجو در این فیلدها
    search_fields = ("username", "first_name", "last_name", "phone_number")

    # قابلیت فیلتر بر اساس این فیلدها
    list_filter = ("is_staff", "is_active")

    # قابلیت تغییر چند کاربر به صورت همزمان
    actions = ["activate_users", "deactivate_users"]

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
        ("Username", {"fields": ("username",)}),
        (
            "Personal Info",
            {
                "fields": (
                    "farsi_first_name",
                    "farsi_last_name",
                    "first_name",
                    "last_name",
                    "national_code",
                    "phone_number",
                    "user_group",
                )
            },
        ),
        ("Status", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Dates ", {"fields": ("date_verify",)}),  #'last_login', 'date_joined',
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "farsi_first_name",
                    "farsi_last_name",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "national_code",
                    "phone_number",
                    "user_group",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    ordering = ("username",)
    filter_horizontal = ()


# admin.site.unregister(LinFortiUsers)
admin.site.register(LinFortiUsers, LinFortiUserAdmin)


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("colored_msg", "create_datetime_format")
    search_fields = ("msg", "create_datetime")
    list_display_links = ("colored_msg",)
    list_filter = ("level", "create_datetime")
    list_per_page = DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE

    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = "green"
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = "orange"
        else:
            color = "red"
        return format_html(
            '<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg
        )

    colored_msg.short_description = "متن لاگ"

    # def traceback(self, instance):
    #     return format_html('<pre><code>{content}</code></pre>', content=instance.trace if instance.trace else '')

    def create_datetime_format(self, instance):
        return timezone.localtime(instance.create_datetime).strftime("%Y-%m-%d %X")

    create_datetime_format.short_description = "ایجاد شده در:"

    def has_add_permission(self, request):
        return False

    # اختیاری: غیر فعال کردن دکمه‌های حذف و ویرایش
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(LogEntry, LogEntryAdmin)
