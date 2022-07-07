import uuid
from datetime import datetime
from unittest.mock import patch

from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main import models, views


class UserCreationTestCase(TestCase):
    def test_create(self):
        data = {
            "username": "alice",
            "email": "alice@example.com",
            "password1": "abcdef123456",
            "password2": "abcdef123456",
        }
        response = self.client.post(reverse("user_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.User.objects.get(username=data["username"]))
        models.User.objects.filter(username="alice").delete()

    def test_create_invalid(self):
        data = {
            "username": "alicewith$symbol",
            "email": "alice@example.com",
            "password1": "abcdef123456",
            "password2": "abcdef123456",
        }
        response = self.client.post(reverse("user_create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Invalid value. Should include only lowercase letters, numbers, and -",
        )
        self.assertEqual(models.User.objects.all().count(), 0)


class UserDeletionTestCase(TestCase):
    def setUp(self):
        data = {
            "username": "alice",
            "email": "alice@example.com",
        }
        self.user = models.User.objects.create(**data)

    def test_delete(self):
        self.client.force_login(self.user)
        self.client.post(reverse("user_delete"))
        self.assertEqual(models.User.objects.filter(username="alice").count(), 0)

    def test_delete_anon(self):
        response = self.client.post(reverse("user_delete"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        self.assertEqual(models.User.objects.filter(username="alice").count(), 1)


class UserUpdateTestCase(TestCase):
    def setUp(self):
        data = {
            "username": "alice",
            "email": "alice@example.com",
        }
        self.user = models.User.objects.create(**data)

    def test_update(self):
        self.client.force_login(self.user)
        data = {
            "username": "bob",
            "email": "bob@example.com",
            "full_name": "Bob ex-Alice",
            "about": "Hey",
            "is_public": True,
        }
        response = self.client.post(reverse("user_update"), data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(models.User.objects.filter(username="alice").exists())
        self.assertEqual(
            models.User.objects.get(username="bob").email, "bob@example.com"
        )
        self.assertEqual(
            models.User.objects.get(username="bob").full_name, "Bob ex-Alice"
        )
        self.assertEqual(models.User.objects.get(username="bob").about, "Hey")
        self.assertEqual(models.User.objects.get(username="bob").is_public, True)

    def test_update_anon(self):
        data = {
            "email": "bob@example.com",
        }
        response = self.client.post(reverse("user_update"), data)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        self.assertEqual(
            models.User.objects.get(username="alice").email, "alice@example.com"
        )


class UserDetailTestCase(TestCase):
    def setUp(self):
        data = {
            "username": "alice",
            "email": "alice@example.com",
        }
        self.user = models.User.objects.create(**data)

    def test_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("user_detail", args=(self.user.username,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_detail_anon(self):
        response = self.client.get(reverse("user_detail", args=(self.user.username,)))
        self.assertEqual(response.status_code, 403)

    def test_detail_anon_public(self):
        data = {
            "username": "bob",
            "email": "bob@example.com",
            "is_public": True,
        }
        self.user_b = models.User.objects.create(**data)
        response = self.client.get(reverse("user_detail", args=(self.user_b.username,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_b.username)


class UserLoginTestCase(TestCase):
    def setUp(self):
        user = models.User.objects.create(username="alice")
        user.set_password("abcdef123456")
        user.save()

    def test_login(self):
        data = {
            "username": "alice",
            "password": "abcdef123456",
        }
        response_login = self.client.post(reverse("login"), data)
        self.assertEqual(response_login.status_code, 302)
        response_index = self.client.get(reverse("index"))
        user = response_index.context.get("user")
        self.assertTrue(user.is_authenticated)

    def test_login_invalid(self):
        data = {
            "username": "alice",
            "password": "wrong_password",
        }
        response_login = self.client.post(reverse("login"), data)
        self.assertEqual(response_login.status_code, 200)
        response_index = self.client.get(reverse("index"))
        self.assertEqual(response_index.status_code, 200)
        user = response_index.context.get("user")
        self.assertFalse(user.is_authenticated)


class LogoutTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice")
        self.client.force_login(self.user)

    def test_logout(self):
        response_logout = self.client.get(reverse("logout"))
        self.assertEqual(response_logout.status_code, 302)
        response_index = self.client.get(reverse("index"))
        user = response_index.context.get("user")
        self.assertFalse(user.is_authenticated)


class StaticTestCase(TestCase):
    def test_index_get(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_coc(self):
        response = self.client.get(reverse("coc"))
        self.assertEqual(response.status_code, 200)

    def test_index_get_workshop(self):
        workshop = models.Workshop.objects.create(
            title="Django",
            slug="django",
            body="details about django",
            scheduled_at=datetime(2020, 2, 18, 13, 15, 0, tzinfo=timezone.utc),
        )
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About")
        self.assertContains(response, "Django")
        workshop.delete()

    def test_workshop_list(self):
        workshop = models.Workshop.objects.create(
            title="Django",
            slug="django",
            body="details about django",
            scheduled_at=datetime(2020, 2, 18, 13, 15, 0, tzinfo=timezone.utc),
        )
        response = self.client.get(reverse("workshop_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django")
        workshop.delete()

    def test_workshop_list_ics(self):
        workshop = models.Workshop.objects.create(
            title="Django",
            slug="django",
            body="details about django",
            scheduled_at=datetime(2020, 2, 18, 13, 15, 0, tzinfo=timezone.utc),
        )
        response = self.client.get(reverse("workshop_list_ics"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django")
        workshop.delete()


class WorkshopTestCase(TestCase):
    def setUp(self):
        self.workshop = models.Workshop.objects.create(
            title="Django",
            slug="django",
            body="details about django",
            scheduled_at=datetime(2020, 2, 18, 13, 15, 0, tzinfo=timezone.utc),
        )

    def test_workshops_get(self):
        response = self.client.get(reverse("workshop", args=(self.workshop.slug,)))
        self.assertEqual(response.status_code, 200)

    def test_workshops_ics_get(self):
        response = self.client.get(reverse("workshop_ics", args=(self.workshop.slug,)))
        self.assertEqual(response.status_code, 200)


class SubscriptionTestCase(TestCase):
    def test_subscribe_get(self):
        response = self.client.get(reverse("subscribe"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subscribe")

    def test_index_post(self):
        response = self.client.post(
            reverse("index"),
            {
                "email": "tester@example.com",
            },
            follow=True,
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


class UnsubscribeInvalidTestCase(TestCase):
    def setUp(self):
        self.subscription = models.Subscription.objects.create(
            email="tester@example.com"
        )

    def test_unsubscribe_invalid_get(self):
        random_uuid = str(uuid.uuid4())
        response = self.client.get(
            reverse("unsubscribe_key", args=(random_uuid,)),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid link")
        self.assertTrue(
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


class FeedbackTestCase(TestCase):
    def test_feedback_get(self):
        response = self.client.get(
            reverse("feedback"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feedback")

    def test_feedback_post(self):
        response = self.client.post(
            reverse("feedback"),
            {
                "comment": "That was medium",
            },
            follow=True,
        )

        # verify request
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank")

        # verify model
        self.assertEqual(models.Feedback.objects.all().count(), 1)
        self.assertEqual(
            models.Feedback.objects.all()[0].comment,
            "That was medium",
        )

        # verify email message
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("New feedback", mail.outbox[0].subject)
        self.assertIn("That was medium", mail.outbox[0].body)

        # verify email headers
        self.assertEqual(mail.outbox[0].to, [settings.ADMINS[0][1]])
        self.assertEqual(
            mail.outbox[0].from_email,
            settings.SERVER_EMAIL,
        )


class BroadcastAnonTestCase(TestCase):
    def setUp(self):
        self.workshop = models.Workshop.objects.create(
            slug="workshop-1",
            title="Django Workshop",
            scheduled_at=timezone.now(),
            location_name="Newspeak House",
            location_address="E2",
            location_url="https://g.co/",
        )
        self.subscription = models.Subscription.objects.create(
            email="tester@example.com"
        )

    def test_broadcast_get(self):
        response = self.client.get(
            reverse("broadcast"),
        )
        self.assertEqual(response.status_code, 403)


class BroadcastUserTestCase(TestCase):
    def setUp(self):
        self.workshop = models.Workshop.objects.create(
            slug="workshop-1",
            title="Django Workshop",
            scheduled_at=timezone.now(),
            location_name="Newspeak House",
            location_address="E2",
            location_url="https://g.co/",
        )
        self.subscription = models.Subscription.objects.create(
            email="tester@example.com"
        )
        self.user = models.User.objects.create(username="alice")
        self.client.force_login(self.user)

    def test_broadcast_get(self):
        response = self.client.get(
            reverse("broadcast"),
        )
        self.assertEqual(response.status_code, 403)


class BroadcastTestCase(TestCase):
    def setUp(self):
        self.workshop = models.Workshop.objects.create(
            slug="workshop-1",
            title="Django Workshop",
            scheduled_at=timezone.now(),
            location_name="Newspeak House",
            location_address="E2",
            location_url="https://g.co/",
        )
        self.subscription = models.Subscription.objects.create(
            email="tester@example.com"
        )
        self.user = models.User.objects.create(username="alice", is_superuser=True)
        self.client.force_login(self.user)

    def test_broadcast_get(self):
        response = self.client.get(
            reverse("broadcast"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Broadcast")

    def test_broadcast_dry_run_post(self):
        with patch.object(
            # Django default test runner overrides SMTP EmailBackend with locmem,
            # but because we re-import the SMTP backend in
            # views.mail.get_connection, we need to mock it here too.
            views.mail,
            "get_connection",
            return_value=mail.get_connection(
                "django.core.mail.backends.locmem.EmailBackend"
            ),
        ):
            response = self.client.post(
                reverse("broadcast"),
                {
                    "subject": "Workshop Announcement",
                    "body": "Hey! We're having a workshop :D",
                    "dry_run": True,
                    "ics_attachment": "workshop-1",
                },
                follow=True,
            )

            # verify request
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "1 emails sent.")

            # verify model
            self.assertEqual(models.EmailRecord.objects.all().count(), 1)
            self.assertEqual(
                models.EmailRecord.objects.all()[0].email,
                settings.EMAIL_BROADCAST_PREVIEW,
            )
            self.assertEqual(
                models.EmailRecord.objects.all()[0].subject,
                "Workshop Announcement",
            )
            self.assertIn(
                "Hey! We're having a workshop :D",
                models.EmailRecord.objects.all()[0].body,
            )
            self.assertIsNone(
                models.EmailRecord.objects.all()[0].subscription,
            )
            self.assertNotEqual(
                models.EmailRecord.objects.all()[0].sent_at,
                None,
            )

    def test_broadcast_post(self):
        with patch.object(
            # Django default test runner overrides SMTP EmailBackend with locmem,
            # but because we re-import the SMTP backend in
            # views.mail.get_connection, we need to mock it here too.
            views.mail,
            "get_connection",
            return_value=mail.get_connection(
                "django.core.mail.backends.locmem.EmailBackend"
            ),
        ):
            response = self.client.post(
                reverse("broadcast"),
                {
                    "subject": "Workshop Announcement",
                    "body": "Hey! We're having a workshop :D",
                    "dry_run": False,
                    "ics_attachment": "workshop-1",
                },
                follow=True,
            )

            # verify request
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "1 emails sent.")

            # verify model
            self.assertEqual(models.EmailRecord.objects.all().count(), 1)
            self.assertEqual(
                models.EmailRecord.objects.all()[0].email,
                "tester@example.com",
            )
            self.assertEqual(
                models.EmailRecord.objects.all()[0].subject,
                "Workshop Announcement",
            )
            self.assertIn(
                "Hey! We're having a workshop :D",
                models.EmailRecord.objects.all()[0].body,
            )
            self.assertEqual(
                models.EmailRecord.objects.all()[0].subscription,
                self.subscription,
            )
            self.assertNotEqual(
                models.EmailRecord.objects.all()[0].sent_at,
                None,
            )


class AttendanceTestCase(TestCase):
    def setUp(self):
        self.workshop = models.Workshop.objects.create(
            title="Django",
            slug="django",
            body="details about django",
            scheduled_at=datetime(2020, 2, 18, 13, 15, 0, tzinfo=timezone.utc),
        )

    def test_rsvp(self):
        response = self.client.post(
            reverse("workshop", args=(self.workshop.slug,)),
            {
                "email": "attendee@example.com",
            },
            follow=True,
        )

        # verify request
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "See you there")

        # verify model
        self.assertEqual(models.Attendance.objects.all().count(), 1)
        self.assertEqual(
            models.Attendance.objects.all()[0].email, "attendee@example.com"
        )

        self.assertEqual(len(mail.outbox), 2)
        # verify email subjects
        subjects = [record.subject for record in mail.outbox]
        self.assertIn(f"See you at: {self.workshop.title}", subjects)
        self.assertIn(
            f"[chaitin] RSVP <attendee@example.com> for {self.workshop.title}", subjects
        )

        # verify email bodies
        bodies = [record.body for record in mail.outbox]
        self.assertTrue(
            any(
                [
                    "attendee@example.com" in bodies[0],
                    "attendee@example.com" in bodies[1],
                ]
            )
        )
        self.assertTrue(
            all([self.workshop.title in bodies[0], self.workshop.title in bodies[1]])
        )

        # verify email recipients
        recipients = [record.to[0] for record in mail.outbox]
        self.assertIn("attendee@example.com", recipients)
        self.assertIn(settings.ADMINS[0][1], recipients)

        # verify email senders
        senders = [record.from_email for record in mail.outbox]
        self.assertIn(settings.DEFAULT_FROM_EMAIL, senders)
        self.assertIn(settings.SERVER_EMAIL, senders)

        # verify email attachments
        attachments = [record.attachments for record in mail.outbox]
        attachments = [att for att in attachments if len(att) > 0]
        attachment_ics = attachments[0][0]
        self.assertEqual(attachment_ics[0], "chaitin-school-django.ics")
        self.assertIn("BEGIN:VCALENDAR", attachment_ics[1])
        self.assertIn("PRODID:chaitin-school/ics", attachment_ics[1])
        self.assertEqual(attachment_ics[2], "application/octet-stream")


class AttendanceTwiceTestCase(TestCase):
    def setUp(self):
        self.workshop = models.Workshop.objects.create(
            title="Django",
            slug="django",
            body="details about django",
            scheduled_at=datetime(2020, 2, 18, 13, 15, 0, tzinfo=timezone.utc),
        )
        self.attendance = models.Attendance.objects.create(
            workshop=self.workshop,
            email="attendee@example.com",
        )

    def test_rsvp_twice(self):
        response = self.client.post(
            reverse("workshop", args=(self.workshop.slug,)),
            {
                "email": "attendee@example.com",
            },
            follow=True,
        )

        # verify request
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Already RSVPed.")

        # verify model
        self.assertEqual(models.Attendance.objects.all().count(), 1)

        self.assertEqual(len(mail.outbox), 2)
        # verify email subjects
        subjects = [record.subject for record in mail.outbox]
        self.assertIn(f"See you at: {self.workshop.title}", subjects)
        self.assertIn(
            f"[chaitin] RSVP <attendee@example.com> for {self.workshop.title}", subjects
        )


class AnnounceAnonTestCase(TestCase):
    def setUp(self):
        self.workshop = models.Workshop.objects.create(
            title="Django",
            slug="django",
            body="details about django",
            scheduled_at=datetime(2020, 2, 18, 13, 15, 0, tzinfo=timezone.utc),
        )

    def test_announce_get(self):
        response = self.client.get(reverse("announce", args=(self.workshop.slug,)))
        self.assertEqual(response.status_code, 403)


class AnnounceUserTestCase(TestCase):
    def setUp(self):
        self.workshop = models.Workshop.objects.create(
            title="Django",
            slug="django",
            body="details about django",
            scheduled_at=datetime(2020, 2, 18, 13, 15, 0, tzinfo=timezone.utc),
        )
        self.user = models.User.objects.create(username="alice")
        self.client.force_login(self.user)

    def test_announce_get(self):
        response = self.client.get(reverse("announce", args=(self.workshop.slug,)))
        self.assertEqual(response.status_code, 403)


class AnnounceSuperuserTestCase(TestCase):
    def setUp(self):
        self.workshop = models.Workshop.objects.create(
            slug="workshop-1",
            title="Django Workshop",
            scheduled_at=timezone.now(),
            location_name="Newspeak House",
            location_address="E2",
            location_url="https://g.co/",
        )
        self.subscription = models.Subscription.objects.create(
            email="tester@example.com"
        )
        self.user = models.User.objects.create(username="alice", is_superuser=True)
        self.client.force_login(self.user)

    def test_announce_get(self):
        response = self.client.get(reverse("announce", args=(self.workshop.slug,)))
        self.assertEqual(response.status_code, 200)

    def test_announce_dry_run_post(self):
        with patch.object(
            # Django default test runner overrides SMTP EmailBackend with locmem,
            # but because we re-import the SMTP backend in
            # views.mail.get_connection, we need to mock it here too.
            views.mail,
            "get_connection",
            return_value=mail.get_connection(
                "django.core.mail.backends.locmem.EmailBackend"
            ),
        ):
            response = self.client.post(
                reverse("announce", args=(self.workshop.slug,)),
                {
                    "subject": "Workshop Announcement",
                    "body": "Hey! We're having a workshop :D",
                    "dry_run": True,
                },
                follow=True,
            )

            # verify request
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "1 emails sent.")

            # verify model
            self.assertEqual(models.EmailRecord.objects.all().count(), 1)
            self.assertEqual(
                models.EmailRecord.objects.all()[0].email,
                settings.EMAIL_BROADCAST_PREVIEW,
            )
            self.assertEqual(
                models.EmailRecord.objects.all()[0].subject,
                "Workshop Announcement",
            )
            self.assertIn(
                "Hey! We're having a workshop :D",
                models.EmailRecord.objects.all()[0].body,
            )
            self.assertIsNone(
                models.EmailRecord.objects.all()[0].subscription,
            )
            self.assertNotEqual(
                models.EmailRecord.objects.all()[0].sent_at,
                None,
            )

    def test_announce_post(self):
        with patch.object(
            # Django default test runner overrides SMTP EmailBackend with locmem,
            # but because we re-import the SMTP backend in
            # views.mail.get_connection, we need to mock it here too.
            views.mail,
            "get_connection",
            return_value=mail.get_connection(
                "django.core.mail.backends.locmem.EmailBackend"
            ),
        ):
            response = self.client.post(
                reverse("announce", args=(self.workshop.slug,)),
                {
                    "subject": "Workshop Announcement",
                    "body": "Hey! We're having a workshop :D",
                    "dry_run": False,
                },
                follow=True,
            )

            # verify request
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "1 emails sent.")

            # verify model
            self.assertEqual(models.EmailRecord.objects.all().count(), 1)
            self.assertEqual(
                models.EmailRecord.objects.all()[0].email,
                "tester@example.com",
            )
            self.assertEqual(
                models.EmailRecord.objects.all()[0].subject,
                "Workshop Announcement",
            )
            self.assertIn(
                "Hey! We're having a workshop :D",
                models.EmailRecord.objects.all()[0].body,
            )
            self.assertEqual(
                models.EmailRecord.objects.all()[0].subscription,
                self.subscription,
            )
            self.assertNotEqual(
                models.EmailRecord.objects.all()[0].sent_at,
                None,
            )


class MentorshipTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(username="alice")
        self.mentorship = models.Mentorship.objects.create(
            mentor=self.user,
            title="Django Mentorship",
            slug="django",
            body="details about django",
        )

    def test_mentorship_list(self):
        response = self.client.get(reverse("mentorship_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Mentorship")

    def test_mentorship_detail(self):
        response = self.client.get(
            reverse("mentorship_detail", args=(self.mentorship.slug,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Mentorship")
