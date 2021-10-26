import uuid

from django.db import models


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unsubscribe_key = models.UUIDField(default=uuid.uuid4, unique=True)

    # def get_unsubscribe_url(self):
    #    path = reverse("unsubscribe_key", args={self.unsubscribe_key})
    #    return f"//{settings.CANONICAL_HOST}{path}"

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=300)
    slug = models.CharField(max_length=300)
    body = models.TextField()
    published_at = models.DateField()

    def __str__(self):
        return self.title
