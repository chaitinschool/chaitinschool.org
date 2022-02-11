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


admin.site.register(models.Submission, SubmissionAdmin)


class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "topic",
    )

    ordering = ["-id"]


admin.site.register(models.Proposal, ProposalAdmin)


class EmailRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "subscription",
        "subject",
    )

    ordering = ["-id"]


admin.site.register(models.EmailRecord, EmailRecordAdmin)
