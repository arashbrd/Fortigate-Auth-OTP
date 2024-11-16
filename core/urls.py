# core/urls.py
from django.contrib import admin
from django.urls import path, include  # Include the include function

urlpatterns = [
    path("", include("usrsmgmnt.urls")),  # Include the 'usersmgmnt' app URLs
    path("admin/", admin.site.urls),
]
