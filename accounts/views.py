from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from accounts.models import Token
from django.urls import reverse
from django.contrib.auth import logout

# Create your views here.

def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login')+'?token=' + str(token.uid)
    )
    message_body = 'Use this link to log in:\n\n %s' %(url)
    send_mail(
        'Your login link for superlists',
        message_body,
        'kozatdd@gmail.com',
        [email]
    )
    messages.success(
        request,
        'Check your email, we have sent you a link you can use to log in.'
    )
    return redirect('/')

def login(request):
    print('Widok login')
    user = auth.authenticate(request, uid=request.GET.get('token'))
    print(user)
    if user:
        print('Login jest user')
        auth.login(request, user)
    return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')
