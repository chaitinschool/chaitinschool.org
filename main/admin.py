from django.contrib import admin

from main import models


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


@admin.register(models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "submitter",
        "email",
        "links",
        "title",
        "when",
    )

    ordering = ["-id"]


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "comment",
    )

    ordering = ["-id"]


@admin.register(models.Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "topic",
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
