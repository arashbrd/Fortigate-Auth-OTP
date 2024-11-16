import logging

logger = logging.getLogger("db")


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]  # اولین آی‌پی در صورت استفاده از پروکسی
        else:
            ip = request.META.get(
                "REMOTE_ADDR"
            )  # آی‌پی مستقیم در صورت عدم استفاده از پروکسی
    except Exception as e:
        logger.exception(f"Error in Getting IP address-->{e}")

        ip = "--UNDEFINED--"
    return ip
