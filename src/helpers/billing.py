import stripe
from decouple import config

DJANGO_DEBUG = config("DJANGO_DEBUG", default=False, cast=str)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", cast=str, default="")

if "sk_test" in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise ValueError("You can't use test api key in production")

stripe.api_key = STRIPE_SECRET_KEY


def create_customer(name="", email="", raw=False, metadata={}):
    response = stripe.Customer.create(
        name=name,
        email=email,
        metadata=metadata,
    )
    if raw:
        return response
    return response.id
