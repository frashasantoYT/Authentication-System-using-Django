from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User 
from django.contrib import messages
from login import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'fom/home.html')
@login_required
def product(request):
    return render(request, 'fom/index.html')
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            messages.success(request, f' {username} you have logged in successfully')
            return redirect('product')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')
        
        
    return render(request, 'fom/signin.html')
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if User.objects.filter(username = username):
            messages.error(request, f'The username {username} already exists')
            return redirect('signup')
        if User.objects.filter(email = email):
             messages.error(request, f'The email {email} already has an account')
             return redirect('signup')
        if pass1 != pass2:
            messages.error(request,'passwords did not match')
            return redirect('signup')
        if len(username) > 15:
            messages.error(request, 'username should have less than 15 characters')
            return redirect('signup')
        
                   
        
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, f'Account for {username} has been successfully created')
        
        subject = 'Welcome to FrashaWeb solutions'
        message = " hello \n Welcome to FrashaWebSolutions \n Thank you for visiting our website\n We have sent you a confirmation email address\n Please confirm your email address to confirm your email address"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email, to_list,fail_silently = True)
        
        
        return redirect('signin')
        
    return render(request, 'fom/signup.html')
def signout(request):
    logout(request)
    messages.success(request, 'Hello you have been successfully logged out')
    return redirect('home')
    
    
