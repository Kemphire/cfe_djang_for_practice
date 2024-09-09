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


def create_product(name="", metadata={}, raw=False):
    response = stripe.Product.create(
        name=name,
        metadata=metadata,
    )
    if raw:
        return response
    stripe_id = response.id
    return stripe_id


def create_price(
    currency="usd",
    unit_amount="9999",
    interval="month",
    product=None,
    metadata={},
    raw=False,
):
    if product is None:
        return None
    response = stripe.Price.create(
        currency=currency,
        unit_amount=unit_amount,
        recurring={"interval": interval},
        product=product,
        metadata=metadata,
    )
    if raw:
        return response
    return response.id  # response.id is stripe id


def start_checkout_session(
    customer_id,
    success_url,
    line_items,
    mode,
    raw=True,
    price_stripe_id="",
    return_url="",
):
    if not success_url.endswith("?session_id={CHECKOUT_SESSION_ID}"):
        success_url = f"{success_url}" + "?session_id={CHECKOUT_SESSION_ID}"
    response = stripe.checkout.Session.create(
        customer_id=customer_id,
        success_url="https://example.com/success",
        line_items=[{"price": price_stripe_id, "quantity": 1}],
        mode="subscription",
        return_url=return_url,
    )
    if raw:
        return response
    return response.url
