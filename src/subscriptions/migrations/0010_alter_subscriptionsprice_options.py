# Generated by Django 5.1 on 2024-09-07 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0009_remove_subscriptions_price"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscriptionsprice",
            options={
                "ordering": ["subscription__order", "order", "featured", "-updated"]
            },
        ),
    ]