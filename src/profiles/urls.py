from django.urls import path
from .views import profile_list_view, profile_detail_view


urlpatterns = [
    path("<str:username>/", profile_detail_view),
    path("list", profile_list_view),
]
