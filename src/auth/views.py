from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("logined here!")
            return redirect("/")
    return render(request, "auth/login.html",{})


def register_view(request):
    return render(request, "auth/login.html",{})
