from django.contrib import admin

from .models import Plan, Service, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "service",
        "plan",
        "price",
        "comment",
    )


admin.site.register(Plan)
admin.site.register(Service)
