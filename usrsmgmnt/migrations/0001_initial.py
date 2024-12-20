# Generated by Django 5.1.2 on 2024-11-15 12:30

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
import django_jalali.db.models
import utils.others.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="FortiGateUserGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "fortigate_id",
                    models.IntegerField(unique=True, verbose_name="شناسه FortiGate"),
                ),
                (
                    "fortigate_name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="نام گروه"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("logger_name", models.CharField(max_length=100)),
                (
                    "level",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "NotSet"),
                            (20, "Info"),
                            (30, "Warning"),
                            (10, "Debug"),
                            (40, "Error"),
                            (50, "Fatal"),
                        ],
                        db_index=True,
                        default=40,
                        verbose_name="سطح",
                    ),
                ),
                ("msg", models.TextField(verbose_name="متن لاگ")),
                ("trace", models.TextField(blank=True, null=True)),
                (
                    "create_datetime",
                    django_jalali.db.models.jDateTimeField(
                        auto_now_add=True, verbose_name="تاریخ"
                    ),
                ),
                ("module", models.CharField(max_length=255)),
                ("function", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": " لاگ",
                "verbose_name_plural": " لاگ\u200cها",
                "ordering": ("-create_datetime",),
            },
        ),
        migrations.CreateModel(
            name="LinFortiUsers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        help_text="نام کاربری ترکیبی از نام خانوادگی لاتین و چهار رقم آخر کد ملی میباشد",
                        max_length=150,
                        unique=True,
                        validators=[utils.others.validators.validate_linux_username],
                        verbose_name="نام کاربری",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        help_text="Enter the first name of the user",
                        max_length=150,
                        validators=[utils.others.validators.validate_english_alphabet],
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        help_text="Enter the last name of the user",
                        max_length=150,
                        validators=[utils.others.validators.validate_english_alphabet],
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text=" نشان می\u200cدهد که آیا این کاربر اجازهٔ فعالیت دارد یا خیر. به جای حذف کاربر این تیک را بردارید.در صورت فعال نبودن کاربر پیامک اطلاع رسانی برای او ارسال نمیگردد",
                        verbose_name="فعال",
                    ),
                ),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "date_verify",
                    django_jalali.db.models.jDateTimeField(
                        blank=True, null=True, verbose_name="تاریخ تایید"
                    ),
                ),
                (
                    "national_code",
                    models.CharField(
                        max_length=10,
                        unique=True,
                        validators=[utils.others.validators.validate_national_code],
                        verbose_name="کد ملی ",
                    ),
                ),
                (
                    "farsi_first_name",
                    models.CharField(max_length=30, verbose_name="نام به فارسی"),
                ),
                (
                    "farsi_last_name",
                    models.CharField(
                        max_length=50, verbose_name=" نام خانوادگی به فارسی"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        help_text="فرمت شماره موبایل به صورت 09123456789 قابل قبول است",
                        max_length=11,
                        unique=True,
                        validators=[utils.others.validators.validate_phone_number],
                        verbose_name=" شماره موبایل",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "user_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="usrsmgmnt.fortigateusergroup",
                        verbose_name="گروه کاربری FortiGate",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
