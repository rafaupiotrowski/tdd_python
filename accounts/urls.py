from django.urls import path, re_path, include
from accounts import views
#from django.contrib.auth import logout

urlpatterns = [
    path('send_login_email', views.send_login_email, name = 'send_login_email'),
    re_path('login+', views.login, name = 'login'),
    path('logout', views.logout_view, name = 'logout')
]