"""
>> LOGIC FOR LOGIN PAGE OF EDIFYLABS BUSINESS TOOL 
"""

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notes


# notes - notes@123
# Tanmay - TanCodes@23


# @login_required(login_url='loginPage')
# def home(request):
#     auth_user = request.user

#     context = {"auth_user": auth_user, "page": "OkNoted | HOME"}
#     return render(request, "home.html", context)


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        pwd = request.POST.get("pwd")
        pwdfinal = request.POST.get("pwdfinal")
        print("this is user name", name)
        if not name or not email or not pwd or not pwdfinal:
            context = {"Error_message": True, "page": "OkNoted | SIGNUP"}
            return render(request, "signup.html", context)
        elif User.objects.filter(username=name).first():
            messages.error(request, "This username is already taken")
            print(User.objects.filter(username=name).first())
            return render(request, "signup.html", {"page": "OkNoted | SIGNUP"})
        else:
            if pwd == pwdfinal:
                users = User.objects.create_user(name, email, pwdfinal)
                users.save()
                context = {"success_signup": True}
                return render(request, "login.html", context)
            return render(request, "signup.html", {"pass_error": "pass_error", "page": "OkNoted | SIGNUP"})

    else:
        return render(request, "signup.html", {"page": "OkNoted | SIGNUP"})


def LoginPage(request):
    page = "LOGIN | Edify Lab's Business Tool"
    if request.method == "POST":
        login_username = request.POST.get('login_username')
        login_pass = request.POST.get('login_pass')

        if not login_username and not login_pass:
            context = {"Error_message": True, "page": page}
            return render(request, "login.html", context)
        else:
            user1 = authenticate(
                request, username=login_username, password=login_pass)

            if user1 is not None:
                login(request, user1)
                return redirect('home')
            else:
                context = {"Error_message_unauthorized": True,
                           "page": page}
                return render(request, "login.html", context)

    else:
        auth_user = request.user
        print("NOT A POST REQUEST", auth_user)
        return render(request, "login.html", {"page": page})


@login_required(login_url='loginPage')
def logoutPage(request):
    logout(request)
    return redirect("loginPage")


def ourstory(request):
    return render(request, "ourstory.html")


