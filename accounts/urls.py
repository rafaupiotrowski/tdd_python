from django.conf.urls import url
from accounts import views

urlpatterns = [
    url('send_email', views.send_login_email, name = 'send_login_email'),
    url('login', views.login, name = 'login'),
    url('logout', views.logout, name = 'logout'),
    
]