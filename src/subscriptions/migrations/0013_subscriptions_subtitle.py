# Generated by Django 5.1 on 2024-09-07 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0012_remove_subscriptionsprice_features_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptions",
            name="subtitle",
            field=models.TextField(blank=True, null=True),
        ),
    ]
