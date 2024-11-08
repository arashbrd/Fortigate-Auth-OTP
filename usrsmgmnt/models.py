# models.py
import logging
from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import AbstractUser
from utils.others.validators import validate_linux_username,validate_national_code



class LinFortiUsers(AbstractUser):
    
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='لطفاً یک نام کاربری انتخاب کنید که فقط شامل حروف، اعداد و علامات مجاز باشد.',
        verbose_name='نام کاربری',
        validators=[validate_linux_username],
    )
    national_code = models.CharField(max_length=10, unique=True,verbose_name='کد ملی ',validators=[validate_national_code])
    farsi_first_name = models.CharField(max_length=30,verbose_name='نام',blank=False)
    farsi_last_name = models.CharField(max_length=50,verbose_name='نام خانوادگی',blank=False)
    phone_number = models.CharField(max_length=11,verbose_name=' شماره موبایل', unique=True)
    user_group = models.ForeignKey(
        'FortiGateUserGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="گروه کاربری FortiGate"
    )
   
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
