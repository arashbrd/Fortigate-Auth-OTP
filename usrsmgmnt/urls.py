from django.urls import path
from .views import (
    connect_fortigate,
    register_user,
    thank_you,
    home_view,
    download,
    about_us,
)
from .views import education, steps_page, run_steps, forti_user_group


urlpatterns = [
    path("", home_view, name="home"),
    path("download/", download, name="download_software"),
    path("about/", about_us, name="about_us"),
    path("edu/", education, name="education"),
    path("admin/fortigate-connect/", connect_fortigate, name="fortigate_connect"),
    path("register/", register_user, name="register_user"),
    path("thank-you/", thank_you, name="thank_you"),
    path("steps/", steps_page, name="steps-page"),
    path("steps/run/", run_steps, name="run_steps"),
    path("forti-user-group/", forti_user_group, name="admin_run_forti-user-group"),
]
