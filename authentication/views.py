from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail, get_connection
from django.conf import settings
from MySAVA import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from .forms import RegisterForm




# auth/views.py

from django.core.mail import EmailMessage, send_mail, get_connection
from django.conf import settings

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            rform = form.save(commit=False)
            rform.role = "USER"
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            messages.success(request, f"New account created: {email}")
            return redirect('welcome')
    else:
        form = RegisterForm()        
    return render(request, "auth/signup.html", {'form':form})


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'auth/activation_failed.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        pass1 = request.POST['password']
        
        user = authenticate(email=email, password=pass1)
        
        if user is not None:
            login(request, user)
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect('welcome')
        else:
            messages.error(request, "Bad Credentials!!")
    
    return render(request, "auth/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')