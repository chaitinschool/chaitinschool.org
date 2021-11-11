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

    def test_index_get_workshop(self):
        models.Workshop.objects.create(
            title="Django",
            slug="django",
            body="details about django",
            transpired_at=datetime(2020, 2, 18),
        )
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Workshops")
        self.assertContains(response, "Django")


class WorkshopTestCase(TestCase):
    def setUp(self):
        self.workshop = models.Workshop.objects.create(
            title="Django",
            slug="django",
            body="details about django",
            transpired_at=datetime(2020, 2, 18),
        )

    def test_workshops_get(self):
        response = self.client.get(
            reverse("workshop_detail", args=(self.workshop.slug,))
        )
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


class SubmissionTestCase(TestCase):
    def test_submission_get(self):
        response = self.client.get(
            reverse("submit"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submit a workshop")

    def test_submission_post(self):
        response = self.client.post(
            reverse("submit"),
            {
                "submitter": "Gregory",
                "email": "gregory@example.com",
                "links": "http://gregory.chaitin/",
                "title": "Complexity",
                "topic": "It's about Kolmogorov complexity",
                "audience": "Everyone",
                "outcome": "Fun",
                "when": "Tomorrow",
            },
            follow=True,
        )

        # verify request
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank you! We’ll be in touch :)")

        # verify model
        self.assertEqual(models.Submission.objects.all().count(), 1)
        self.assertEqual(models.Submission.objects.all()[0].submitter, "Gregory")
        self.assertEqual(
            models.Submission.objects.all()[0].email, "gregory@example.com"
        )
        self.assertEqual(
            models.Submission.objects.all()[0].links, "http://gregory.chaitin/"
        )
        self.assertEqual(models.Submission.objects.all()[0].title, "Complexity")
        self.assertEqual(
            models.Submission.objects.all()[0].topic, "It's about Kolmogorov complexity"
        )
        self.assertEqual(models.Submission.objects.all()[0].audience, "Everyone")
        self.assertEqual(models.Submission.objects.all()[0].outcome, "Fun")
        self.assertEqual(models.Submission.objects.all()[0].when, "Tomorrow")

        # verify email message
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "New submission: Gregory <gregory@example.com>", mail.outbox[0].subject
        )
        self.assertIn("Complexity", mail.outbox[0].body)
        self.assertIn("It's about Kolmogorov complexity", mail.outbox[0].body)
        self.assertIn("Everyone", mail.outbox[0].body)
        self.assertIn("Fun", mail.outbox[0].body)
        self.assertIn("Tomorrow", mail.outbox[0].body)
        self.assertIn("http://gregory.chaitin/", mail.outbox[0].body)

        # verify email headers
        self.assertEqual(mail.outbox[0].to, [settings.ADMINS[0][1]])
        self.assertEqual(
            mail.outbox[0].from_email,
            settings.SERVER_EMAIL,
        )


class ProposalTestCase(TestCase):
    def test_proposal_get(self):
        response = self.client.get(
            reverse("proposal"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Proposal")

    def test_proposal_post(self):
        response = self.client.post(
            reverse("proposal"),
            {
                "email": "gregory@example.com",
                "topic": "I want to know about Kolmogorov complexity",
            },
            follow=True,
        )

        # verify request
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thanks—we might be in touch.")

        # verify model
        self.assertEqual(models.Proposal.objects.all().count(), 1)
        self.assertEqual(models.Proposal.objects.all()[0].email, "gregory@example.com")
        self.assertEqual(
            models.Proposal.objects.all()[0].topic,
            "I want to know about Kolmogorov complexity",
        )

        # verify email message
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("New proposal: gregory@example.com", mail.outbox[0].subject)
        self.assertIn("I want to know about Kolmogorov complexity", mail.outbox[0].body)

        # verify email headers
        self.assertEqual(mail.outbox[0].to, [settings.ADMINS[0][1]])
        self.assertEqual(
            mail.outbox[0].from_email,
            settings.SERVER_EMAIL,
        )
