# Generated by Django 5.1 on 2024-09-07 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0005_subscriptions_stripe_id_subscriptionsprice"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptionsprice",
            name="featured",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="subscriptionsprice",
            name="order",
            field=models.IntegerField(default=-1),
        ),
    ]