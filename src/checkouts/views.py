from django.shortcuts import redirect, resolve_url

from django.contrib.auth.decorators import login_required
from subscriptions.models import SubscriptionsPrice

from helpers.billing import start_checkout_session
from django.conf import settings

BASE_URL = settings.BASE_URL


def product_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session["checkout_subscription_price_id"] = price_id
    return redirect("stripe-checkout-start")


@login_required
def checkout_redirect_view(request):
    checkout_subscription_price_id = request.session.get(
        "checkout_subscription_price_id"
    )
    try:
        obj = SubscriptionsPrice.objects.get(id=checkout_subscription_price_id)
    except KeyError:
        obj = None
    if checkout_subscription_price_id is None or obj is None:
        return redirect("subscription_pricing_args")
    customer_stripe_id = request.user.customer.stripe_id
    success_url_path = resolve_url("stripe-checkout-end")
    pricing_url_path = resolve_url("subscription_pricing_args")
    success_url = f"{BASE_URL}{success_url_path}"
    return_url = f"{BASE_URL}{pricing_url_path}"
    customer_stripe_id = obj.stripe_id
    price_stripe_id = obj.stripe_id
    url = start_checkout_session(
        customer_id=customer_stripe_id,
        price_stripe_id=price_stripe_id,
        success_url=success_url,
        return_url=return_url,
        raw=False,
    )
    return redirect(url)


def checkout_finalize_view(request): ...
