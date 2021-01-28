from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from . forms import UserLogin
from django.contrib import messages

# Create your views here.

# method used for custom login
def LoginUser(request):
    nexts = request.GET.get("next")
    form = UserLogin()
    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            if nexts:
                return redirect(nexts)
            messages.success(request, "successfully login")
            return redirect("teacher-list")

    context = {"form": form}
    return render(request, "accounts/user_login.html", context)


def LogoutUser(request):
    logout(request)
    return redirect("accounts:user-login")