from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

def login_view(request):
    print(request.method, request.POST or None)
    if request.method == "POST":
        print(request.method, request.POST or None)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("logined here!")
            return redirect("home")
    return render(request, "auth/login.html",{})


def register_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if username and email and password:
            model = get_user_model()
            user_exists = model.objects.filter(username__iexact=username).exists()
            email_exists = model.objects.filter(email__iexact=email).exists()
            if not user_exists or not email_exists:
                ...
            model.objects.create_user(username=username,email=email,password=password)
            return redirect("home")
            
    return render(request, "auth/register.html",{})
