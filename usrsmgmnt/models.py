# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.validators import validate_linux_username,validate_national_code

class LinFortiUsers(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='لطفاً یک نام کاربری انتخاب کنید که فقط شامل حروف، اعداد و علامات مجاز باشد.',
        verbose_name='نام کاربری',
        validators=[validate_linux_username],
    )
    national_code = models.CharField(max_length=10, unique=True,verbose_name='کد ملی ',validators=[validate_national_code])
    phone_number = models.CharField(max_length=11,verbose_name=' شماره موبایل')
    user_group = models.ForeignKey(
        'FortiGateUserGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="گروه کاربری FortiGate"
    )


class FortiGateUserGroup(models.Model):
    fortigate_id = models.CharField(max_length=100, unique=True, verbose_name="شناسه FortiGate")
    fortigate_name = models.CharField(max_length=100, unique=True, verbose_name="نام گروه")
    
    def __str__(self):
        return self.fortigate_name