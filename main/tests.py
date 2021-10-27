from datetime import datetime

from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from main import models


class StaticTestCase(TestCase):
    def test_index_get(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_workshops_get(self):
        response = self.client.get(reverse("workshops"))
        self.assertEqual(response.status_code, 200)


class SubscriptionTestCase(TestCase):
    def test_subscribe_get(self):
        response = self.client.get(
            reverse("index"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subscribe")

    def test_index_post(self):
        response = self.client.post(
            reverse("index"),
            {
                "email": "tester@example.com",
            },
        )

        # verify request
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thanks! Email saved—we’ll be in touch soon!")

        # verify model
        self.assertEqual(models.Subscription.objects.all().count(), 1)
        self.assertEqual(
            models.Subscription.objects.all()[0].email, "tester@example.com"
        )

        # verify email message
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("New subscription: tester@example.com", mail.outbox[0].subject)
        self.assertIn("tester@example.com", mail.outbox[0].body)

        # verify email headers
        self.assertEqual(mail.outbox[0].to, [settings.ADMINS[0][1]])
        self.assertEqual(
            mail.outbox[0].from_email,
            settings.SERVER_EMAIL,
        )


class UnsubscribeTestCase(TestCase):
    def setUp(self):
        self.subscription = models.Subscription.objects.create(
            email="tester@example.com"
        )

    def test_unsubscribe_get(self):
        response = self.client.get(
            reverse("unsubscribe_key", args=(self.subscription.unsubscribe_key,)),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tester@example.com deleted from mailing list.")
        self.assertFalse(
            models.Subscription.objects.filter(id=self.subscription.id).exists()
        )


class BlogTestCase(TestCase):
    def test_blog_index(self):

        models.Post.objects.create(
            title="First post",
            slug="first-post",
            body="I am the body",
            published_at=datetime(2020, 2, 18),
        )
        response = self.client.get(reverse("blog"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First post")

    def test_blog_index_empty(self):
        response = self.client.get(reverse("blog"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nothing published yet")

    def test_post(self):
        post = models.Post.objects.create(
            title="First post",
            slug="first-post",
            body="I am the body",
            published_at=datetime(2020, 2, 18),
        )
        response = self.client.get(reverse("post", args=(post.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First post")
        self.assertContains(response, "I am the body")
