import uuid
from base64 import b64encode

import bleach
import markdown
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

from main import denylist, validators


class User(AbstractUser):
    username = models.CharField(
        max_length=64,
        unique=True,
        help_text="Letters, digits, hyphens only.",
        validators=[
            validators.AlphanumericHyphenValidator(),
            validators.HyphenOnlyValidator(),
        ],
        error_messages={"unique": "A user with that username already exists."},
    )
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    about = models.TextField(blank=True)
    avatar_data = models.BinaryField()
    avatar_ext = models.CharField(max_length=4)
    is_public = models.BooleanField(
        default=False,
        help_text="Enable to make profile available to non-logged-in users.",
    )

    @property
    def displayname(self):
        return "~" + self.username

    @property
    def avatar_base64(self):
        if not self.avatar_data:
            # 1x1 PNG with #f2f2f2 fill
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP89B8AAukB8/71MdcAAAAASUVORK5CYII="
        return b64encode(self.avatar_data).decode("utf-8")

    @property
    def about_as_html(self):
        dirty_html = markdown.markdown(
            self.about,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
                "markdown.extensions.footnotes",
            ],
        )
        return bleach.clean(
            dirty_html,
            tags=denylist.ALLOWED_HTML_ELEMENTS,
            attributes=denylist.ALLOWED_HTML_ATTRS,
        )

    def __str__(self):
        return self.username


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unsubscribe_key = models.UUIDField(default=uuid.uuid4, unique=True)

    def get_unsubscribe_url(self):
        path = reverse("unsubscribe_key", args={self.unsubscribe_key})
        return f"//{settings.CANONICAL_HOST}{path}"

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    byline = models.CharField(max_length=300)
    body = models.TextField()
    published_at = models.DateField(null=True, blank=True)

    @property
    def is_published(self):
        today = timezone.now().date()
        if self.published_at and self.published_at <= today:
            return True
        return False

    @property
    def body_as_html(self):
        return markdown.markdown(
            self.body,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
                "markdown.extensions.footnotes",
            ],
        )

    def __str__(self):
        return self.title


class Workshop(models.Model):
    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    body = models.TextField()
    scheduled_at = models.DateTimeField(null=True, blank=True)
    location_name = models.CharField(max_length=300)
    location_address = models.CharField(max_length=300)
    location_url = models.URLField()

    @property
    def is_future(self):
        if not self.scheduled_at:
            return False
        return timezone.now().date() <= self.scheduled_at.date()

    @property
    def body_as_html(self):
        return markdown.markdown(
            self.body,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
                "markdown.extensions.footnotes",
            ],
        )

    def get_absolute_url(self):
        path = reverse("workshop", kwargs={"slug": self.slug})
        return f"//{settings.CANONICAL_HOST}{path}"

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-scheduled_at"]


class Feedback(models.Model):
    comment = models.TextField()

    def __str__(self):
        return self.comment[:30] + "..."


class EmailRecord(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=300)
    body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now, null=True)

    # email literal field in case subscription foreign key
    # is null which means user has unsubscribed
    email = models.EmailField()

    class Meta:
        ordering = ["-sent_at"]

    def __str__(self):
        return f"Email record: {self.subject}"


class Attendance(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)
    rsvp = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]
        unique_together = [["workshop", "email"]]

    def __str__(self):
        return f"RSVP: {self.email} for {self.workshop.title}"


class Mentorship(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    body = models.TextField()

    @property
    def body_as_html(self):
        return markdown.markdown(
            self.body,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
                "markdown.extensions.footnotes",
            ],
        )

    def __str__(self):
        return self.title
