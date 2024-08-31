from helpers.billing import create_customer
from django.db import models
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

from allauth.account.signals import (
    user_signed_up as allauth_user_signed_up,
    email_confirmed as allauth_email_confirmed,
)

User = settings.AUTH_USER_MODEL


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    init_email = models.EmailField(blank=True, null=True)
    init_email_confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        if not self.stripe_id:
            if self.init_email_confirmed and self.init_email:
                email = self.user.email
                if email != "" or email is not None:
                    stripe_response = create_customer(
                        name=self.user.first_name + " " + self.user.last_name,
                        email=email,
                        raw=False,
                        metadata={"user_id": self.user.id},
                    )
                    self.stripe_id = stripe_response
        super().save(*args, **kwargs)


def is_social_user(user):
    return SocialAccount.objects.filter(user=user).exists()


def allauth_user_signed_up_handler(request, user, *args, **kwargs):
    email = user.email
    email_conf = False
    if (
        is_social_user(user)
        and settings.SOCIALACCOUNT_PROVIDERS["github"]["VERIFIED_EMAIL"]
    ):
        email_conf = True
    Customer.objects.create(
        user=user,
        init_email=email,
        init_email_confirmed=email_conf,
    )


allauth_user_signed_up.connect(allauth_user_signed_up_handler)


def allauth_email_handler(request, email_address, *args, **kwargs):
    qs = Customer.objects.filter(init_email=email_address, init_email_confirmed=False)
    for ins in qs:
        ins.init_email_confirmed = True
        ins.save()


allauth_email_confirmed.connect(allauth_email_handler)
