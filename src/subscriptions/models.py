from django.db import models
from django.contrib.auth.models import Group, Permission

SUBSRIPTION_PERMISSION = [
    ("advanced", "Advanced Perm"),
    ("pro", "Pro perm"),
    ("basic", "Basic perm"),
]


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
