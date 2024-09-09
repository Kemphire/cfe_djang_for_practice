from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.urls import reverse

from django.db.models.signals import post_save

import helpers

SUBSRIPTION_PERMISSION = [
    ("advanced", "Advanced Perm"),
    ("pro", "Pro perm"),
    ("basic", "Basic perm"),
]

ALLOW_CUSTOM_GROUPS = True

User = settings.AUTH_USER_MODEL  # "auth.user"


class Subscriptions(models.Model):
    name = models.CharField(max_length=120)
    groups = models.ManyToManyField(Group)
    active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(
        Permission,
        limit_choices_to={
            "content_type__app_label": "subscriptions",
            "codename__in": [x[0] for x in SUBSRIPTION_PERMISSION],
        },
    )
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    order = models.IntegerField(default=-1, help_text="Odering on django pricing page")
    featured = models.BooleanField(
        default=True,
        help_text="Featured on Django Pricing page, doesn't affect stripe things",
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    features = models.TextField(
        help_text="Features for Subscription seperated by new line",
        blank=True,
        null=True,
    )
    subtitle = models.TextField(blank=True, null=True)

    def get_features_as_list(self):
        if not self.features:
            return []
        return [x.strip() for x in self.features.split("\n")]

    def __str__(self) -> str:
        return self.name.capitalize()

    class Meta:
        permissions = SUBSRIPTION_PERMISSION

    def save(self, *args, **kwargs):
        if not self.stripe_id:
            stripe_id = helpers.billing.create_product(
                name=self.name,
                metadata={
                    "subscription_plan_id": self.id,
                },
                raw=False,
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)


class SubscriptionsPrice(models.Model):
    class IntervalChoices(models.TextChoices):
        MONTHLY = "month", "Monthly"
        YEARLY = "year", "Yearly"

    subscription = models.ForeignKey(
        Subscriptions, on_delete=models.SET_NULL, null=True
    )
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    interval = models.CharField(
        max_length=120, default=IntervalChoices.MONTHLY, choices=IntervalChoices.choices
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    order = models.IntegerField(default=-1, help_text="Odering on django pricing page")
    featured = models.BooleanField(
        default=True,
        help_text="Featured on Django Pricing page, doesn't affect stripe things",
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id

    @property
    def display_sub_name(self):
        if not self.subscription:
            return "Plan"
        return self.subscription.name.title()

    @property
    def stripe_currency(self):
        return "usd"

    @property
    def display_features_list(self):
        if not self.subscription:
            return []
        return self.subscription.get_features_as_list()

    @property
    def display_sub_subtitle(self):
        if not self.subscription:
            return ""
        return self.subscription.subtitle

    @property
    def stripe_price(self):
        """
        For stripe price remove decimal prices
        """
        return int(self.price * 100)

    def get_checkout_url(self):
        return reverse("sub-price-checkout", kwargs={"price_id": self.id})

    class Meta:
        ordering = ["subscription__order", "order", "featured", "-updated"]

    def save(self, *args, **kwargs):
        if self.product_stripe_id is not None and self.stripe_id is None:
            stripe_id = helpers.billing.create_price(
                currency=self.stripe_currency,
                unit_amount=self.stripe_price,
                interval=self.interval,
                product=self.product_stripe_id,
                metadata={
                    "subscription_plan_price_id": self.id,
                },
                raw=False,
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)
        if self.featured:
            qs = SubscriptionsPrice.objects.filter(
                subscription=self.subscription,
                interval=self.interval,
            ).exclude(id=self.id)
            qs.update(featured=False)

    def __str__(self) -> str:
        return f"Price of {self.subscription.name} "


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        Subscriptions, on_delete=models.SET_NULL, null=True, blank=True
    )
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s Subscriptions"


def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    group_id_of_subscription_instance = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        group_id_of_subscription_instance = groups.values_list("id", flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups)
    else:
        subs_qs = Subscriptions.objects.filter(active=True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_group = subs_qs.values_list("groups__id", flat=True)
        subs_group_set = set(subs_group)
        # group_id_of_subscription_instance = groups.values_list("id", flat=True)
        current_group_of_user = user.groups.all().values_list("id", flat=True)
        group_ids_set = set(group_id_of_subscription_instance)
        current_group_set = set(current_group_of_user) - subs_group_set
        final_group_ids = list(group_ids_set | current_group_set)
        user.groups.set(final_group_ids)


post_save.connect(user_sub_post_save, sender=UserSubscription)
