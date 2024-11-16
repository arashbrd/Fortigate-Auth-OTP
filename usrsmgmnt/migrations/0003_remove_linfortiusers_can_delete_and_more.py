# Generated by Django 5.1.2 on 2024-11-15 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usrsmgmnt", "0002_linfortiusers_can_delete"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="linfortiusers",
            name="can_delete",
        ),
        migrations.AddField(
            model_name="linfortiusers",
            name="prevent_delete",
            field=models.BooleanField(default=True),
        ),
    ]
