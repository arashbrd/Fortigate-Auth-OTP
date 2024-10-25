# usersmgmnt/urls.py
from django.urls import path
from .views import connect_fortigate,home  # Import the view
from .views import register_user, thank_you,home_view,download,about_us,education,steps_page,run_steps


urlpatterns = [
    path('', home_view, name='home'),
    path('download/', download, name='download_software'),
    path('about/', about_us, name='about_us'),
    path('edu/', education, name='education'),
    
    path('admin/fortigate-connect/', connect_fortigate, name='fortigate_connect'),
    path('register/', register_user, name='register_user'),
    path('thank-you/', thank_you, name='thank_you'),

    path('steps/', steps_page, name='steps-page'),
    path('steps/run/', run_steps, name='run_steps'),


]
