import uuid

import markdown
from django.conf import settings
from django.db import models
from django.urls import reverse


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
    body = models.TextField()
    published_at = models.DateField()

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
    transpired_at = models.DateField()

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


class Submission(models.Model):
    """Workshop submission."""

    submitter = models.CharField(max_length=300, verbose_name="What’s your name?")
    email = models.EmailField(verbose_name="What’s your email?")
    links = models.TextField(
        blank=True, null=True, verbose_name="Any of website, blog, twitter, github"
    )
    title = models.CharField(max_length=300, verbose_name="Title of your workshop")
    topic = models.TextField(blank=True, null=True, verbose_name="What is it about?")
    audience = models.TextField(blank=True, null=True, verbose_name="Who is it for?")
    outcome = models.TextField(
        blank=True,
        null=True,
        verbose_name="What will the attendees have learned at the end of your workshop?",
    )
    when = models.TextField(
        blank=True,
        null=True,
        verbose_name="When approximately are you thinking of presenting this?",
    )

    def __str__(self):
        return self.title


class Request(models.Model):
    """Request for a workshop."""

    email = models.EmailField(blank=True, null=True)
    topic = models.TextField()

    def __str__(self):
        return self.topic[:30] + "..."
