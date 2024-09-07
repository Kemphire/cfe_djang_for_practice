from django.shortcuts import render

from .models import SubscriptionsPrice


def subscription_price_view(request):
    base_qs = SubscriptionsPrice.objects.filter(featured=True)
    monthly_qs = base_qs.filter(
        interval=SubscriptionsPrice.IntervalChoices.MONTHLY,
    )
    yearly_qs = base_qs.filter(
        interval=SubscriptionsPrice.IntervalChoices.YEARLY,
    )

    return render(
        request,
        "subscriptions/pricing.html",
        {
            "monthly_qs": monthly_qs,
            "yearly_qs": yearly_qs,
        },
    )
