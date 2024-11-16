from django.conf import settings


def app_version(request):
    return {
        "app_version": settings.APP_VERSION,
        "org_name": settings.ORG_NAME,
        "org_website": settings.ORG_WEBSITE,
        "sms_number": settings.SMS_NUMBER,
        "panel_web_address": settings.PANEL_WEB_ADDRESS,
        "panel_name": settings.PANEL_NAME,
    }


def current_path(request):
    return {"current_path": request.path}
