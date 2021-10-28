from django.contrib import admin

from main import models


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "created_at",
        "unsubscribe_key",
    )

    ordering = ["-id"]


admin.site.register(models.Subscription, SubscriptionAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "published_at",
    )

    ordering = ["-id"]


admin.site.register(models.Post, PostAdmin)


class WorkshopAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
    )

    ordering = ["-id"]


admin.site.register(models.Workshop, WorkshopAdmin)
