from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjUserAdmin

from main import models


@admin.register(models.User)
class UserAdmin(DjUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "date_joined",
        "last_login",
        "is_public",
    )
    list_display_links = ("id", "username")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("full_name", "email", "about", "is_public")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    search_fields = ("username", "full_name", "email")

    ordering = ["-id"]


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "created_at",
        "unsubscribe_key",
    )

    ordering = ["-id"]


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "published_at",
    )

    ordering = ["-id"]


@admin.register(models.Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
    )

    ordering = ["-id"]


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "comment",
    )

    ordering = ["-id"]


@admin.register(models.EmailRecord)
class EmailRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "subscription",
        "subject",
    )

    ordering = ["-id"]


@admin.register(models.Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "workshop",
        "email",
        "rsvp",
        "created_at",
    )

    ordering = ["-workshop", "id"]
