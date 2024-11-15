# models.py
import logging
from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import AbstractUser
from utils.others.validators import validate_linux_username,validate_national_code,validate_phone_number,validate_english_alphabet



class LinFortiUsers(AbstractUser):   
    
    username = models.CharField(
        max_length=150,
        unique=True,
        # help_text='لطفاً یک نام کاربری انتخاب کنید که فقط شامل حروف، اعداد و علامات مجاز باشد.',
        verbose_name='نام کاربری',
        validators=[validate_linux_username],
        help_text="نام کاربری ترکیبی از نام خانوادگی لاتین و چهار رقم آخر کد ملی میباشد",
    )
    # Override the `first_name` field to change help_text
    first_name = models.CharField(validators=[validate_english_alphabet],
        max_length=150,
        
        help_text="Enter the first name of the user"
    )
    
    
    # Override the `last_name` field to change help_text
    last_name = models.CharField(validators=[validate_english_alphabet],
        max_length=150,
        
        help_text="Enter the last name of the user"
    )
    is_active = models.BooleanField(verbose_name='فعال',
        default=True,
        help_text=" نشان می‌دهد که آیا این کاربر اجازهٔ فعالیت دارد یا خیر. به جای حذف کاربر این تیک را بردارید."

                  "در صورت فعال نبودن کاربر پیامک اطلاع رسانی برای او ارسال نمیگردد"
    )
    is_verified = models.BooleanField(default=False)
    date_verify=jmodels.jDateTimeField(blank=True, null=True,verbose_name='تاریخ تایید')

    national_code = models.CharField(max_length=10, unique=True,verbose_name='کد ملی ',validators=[validate_national_code])
    farsi_first_name = models.CharField(max_length=30,verbose_name='نام به فارسی',blank=False)
    farsi_last_name = models.CharField(max_length=50,verbose_name=' نام خانوادگی به فارسی',blank=False)
    phone_number = models.CharField(max_length=11,verbose_name=' شماره موبایل', unique=True,validators=[validate_phone_number],help_text="فرمت شماره موبایل به صورت 09123456789 قابل قبول است")
    user_group = models.ForeignKey(
        'FortiGateUserGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="گروه کاربری FortiGate"
    )
    prevent_delete = models.BooleanField(default=True)
    def delete(self, *args, **kwargs):
        if self.prevent_delete:
            print("&&&&&&&&&&&&&&&&&&&&")
            print(f"prevent_delete = {self.prevent_delete}")          
            return
        super().delete(*args, **kwargs)
   
class FortiGateUserGroup(models.Model):
    fortigate_id = models.IntegerField( unique=True, verbose_name="شناسه FortiGate")
    fortigate_name = models.CharField(max_length=100, unique=True, verbose_name="نام گروه")
    
    def __str__(self):
        return self.fortigate_name
     

LOG_LEVELS = (
    (logging.NOTSET, 'NotSet'),
    (logging.INFO, 'Info'),
    (logging.WARNING, 'Warning'),
    (logging.DEBUG, 'Debug'),
    (logging.ERROR, 'Error'),
    (logging.FATAL, 'Fatal'),
)

class LogEntry(models.Model):
    objects = jmodels.jManager()
    logger_name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(choices=LOG_LEVELS, default=logging.ERROR, db_index=True,verbose_name='سطح')
    msg = models.TextField(verbose_name='متن لاگ')
    trace = models.TextField(blank=True, null=True)
    create_datetime = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ')
    module = models.CharField(max_length=255)
    function = models.CharField(max_length=255)

    def __str__(self):
        return self.msg

    class Meta:
        verbose_name = " لاگ"
        verbose_name_plural = " لاگ‌ها"
        ordering = ('-create_datetime',)
