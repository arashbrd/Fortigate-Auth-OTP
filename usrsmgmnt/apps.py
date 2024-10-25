from django.apps import AppConfig


class UsrsmgmntConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usrsmgmnt'
    verbose_name = ' کاربران'

    def ready(self):
        import usrsmgmnt.signals
