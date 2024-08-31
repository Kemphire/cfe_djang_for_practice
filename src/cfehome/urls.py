"""
URL configuration for cfehome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from auth import views as auth_views

from .views import (
    about_view,
    home_view,
    pw_protected_view,
    user_protected_view,
    staff_protected_view,
)

urlpatterns = [
    path("", home_view),  # index page -> root page
    path("about/", about_view, name="about"),
    path("login/", auth_views.login_view, name="login"),
    path("register/", auth_views.register_view, name="register"),
    path("hello-world/", home_view, name="home"),
    path("protected/", pw_protected_view, name="protected"),
    path("user_protected", user_protected_view, name="user_protected"),
    path("staff_protected", staff_protected_view, name="staff_protected"),
    path("hello-world.html", home_view),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("profiles/", include("profiles.urls")),
]
