from django.contrib.auth import authenticate, login as auth_login,logout
from django.shortcuts import render,redirect
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  
            return redirect('main:index')
        else:
            return render(request, 'login/account.html', {'error_message': 'Invalid email or password'})

    return render(request, 'login/account.html')





def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        try:
            if password == password_confirmation:
                user = User.objects.create_user(username=username, password=password)
                return redirect('main:index')
        except IntegrityError:
            return redirect('account:register')
        
    
    return render(request, 'login/register.html')



    





@login_required
def edit_profile(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        email = request.POST['email']
        user = request.user
        user.username = username
        user.first_name = first_name
        user.email = email
        user.save()
    return render(request, 'login/edit.html')


def set_password(request):

    old = request.POST['old']
    new = request.POST['new']
    confirm = request.POST['confirm']
    user = request.user
    if user.check_password(old) and new == confirm:
        user.set_password(new)
        user.save()
    return redirect('account:login/edit_profile')



def logout_user(request):
    user1=request.user
    logout(user1)
    return redirect('login')
