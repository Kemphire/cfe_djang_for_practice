from django.shortcuts import render

from .models import SubscriptionsPrice


def subscription_price_view(request, interval="month"):
    base_qs = SubscriptionsPrice.objects.filter(featured=True)
    interval_monthly = SubscriptionsPrice.IntervalChoices.MONTHLY
    interval_yearly = SubscriptionsPrice.IntervalChoices.YEARLY

    if interval.lower() == "month":
        monthly_qs = base_qs.filter(interval=interval_monthly)
        return render(
            request,
            "subscriptions/pricing.html",
            {
                "subcription_qs": monthly_qs,
                "active": "month",  # to color correct link
            },
        )
    elif interval.lower() == "year":
        yearly_qs = base_qs.filter(interval=interval_yearly)
        return render(
            request,
            "subscriptions/pricing.html",
            {
                "subcription_qs": yearly_qs,
                "active": "year",
            },
        )
    else:
        return render(
            request,
            "subscriptions/pricing.html",
            {"subscription_qs": [], "error": "Invalid argument to this url"},
        )
