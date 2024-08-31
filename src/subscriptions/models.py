from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings

from django.db.models.signals import post_save

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

    def __str__(self) -> str:
        return self.name.capitalize()

    class Meta:
        permissions = SUBSRIPTION_PERMISSION


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
