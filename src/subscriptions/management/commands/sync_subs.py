from django.core.management.base import BaseCommand

from subscriptions.models import Subscriptions


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("How i'm not able to understand it")
        qs = Subscriptions.objects.filter(active=True)
        for obj in qs:
            sub_perms = obj.permissions.all()
            for grp in obj.groups.all():
                grp.permissions.set(sub_perms)
