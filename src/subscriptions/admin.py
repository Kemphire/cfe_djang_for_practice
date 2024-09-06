from django.contrib import admin

from .models import Subscriptions, UserSubscription, SubscriptionsPrice


class SubscriptionPrice(admin.TabularInline):
    model = SubscriptionsPrice
    readonly_fields = ["stripe_id"]
    extra = 0
    can_delete = False


class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPrice]
    list_display = ["name", "active"]
    readonly_fields = ["stripe_id"]


admin.site.register(Subscriptions, SubscriptionAdmin)
admin.site.register(UserSubscription)
