from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from main import models


class StaticTestCase(TestCase):
    def test_index_get(self):
        response = self.client.get(reverse("index"))
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
        # self.assertEqual(len(mail.outbox), 1)
        # self.assertIn("New subscription: tester@example.com", mail.outbox[0].subject)
        # self.assertIn("tester@example.com", mail.outbox[0].body)

        # verify email headers
        # self.assertEqual(mail.outbox[0].to, [settings.ADMINS[0][1]])
        # self.assertEqual(
        #    mail.outbox[0].from_email,
        #    settings.SERVER_EMAIL,
        # )
