from django.urls import path
from .views import subscription_price_view

urlpatterns = [
    path(
        "pricing/<str:interval>/",
        subscription_price_view,
        name="subscription_pricing",
        # it will show monthly and yearly pricing differently depending on the arguments passed
    ),
    path(
        "pricing/",
        subscription_price_view,
        name="subscription_pricing_args",
    ),
]
