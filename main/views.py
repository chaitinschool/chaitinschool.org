from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core import mail
from django.core.mail import mail_admins
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from main import forms, models, utils


def index(request):
    if request.method == "GET" or request.method == "HEAD":
        post_list = models.Post.objects.all().order_by("-published_at")

        today = timezone.now().date()
        past_workshop_list = models.Workshop.objects.filter(
            scheduled_at__date__isnull=False,
            scheduled_at__date__lt=today,
        ).order_by("-scheduled_at")
        future_workshop_list = models.Workshop.objects.filter(
            scheduled_at__date__isnull=False,
            scheduled_at__date__gte=today,
        ).order_by("-scheduled_at")
        draft_workshop_list = models.Workshop.objects.filter(
            scheduled_at__date__isnull=True
        ).order_by("-title")

        return render(
            request,
            "main/index.html",
            {
                "past_workshop_list": past_workshop_list,
                "future_workshop_list": future_workshop_list,
                "draft_workshop_list": draft_workshop_list,
                "post_list": post_list,
            },
        )

    elif request.method == "POST":
        form = forms.SubscriptionForm(request.POST)

        # if post data not valid
        if not form.is_valid():
            if "email" in form.errors and form.errors["email"] == [
                "Subscription with this Email already exists."
            ]:
                # if case of already subscribed
                messages.info(request, "Email already subscribed :)")
                return redirect("index")
            else:
                # all other cases
                messages.error(request, "Something is wrong.")
                return render(
                    request,
                    "main/index.html",
                    {
                        "form": form,
                    },
                )

        # this branch only executes if form is valid
        form.save()
        submitter_email = form.cleaned_data["email"]
        mail_admins(
            f"New subscription: {submitter_email}",
            f"Someone new has subscribed to the {settings.PROJECT_NAME} list. Hooray!\n"
            + f"\nIt's {submitter_email}\n",
        )

        messages.success(request, "Thanks! Email saved—we’ll be in touch soon!")
        return redirect("index")


class AttendanceView(SuccessMessageMixin, FormView):
    form_class = forms.AttendanceForm
    template_name = "main/workshop.html"
    success_message = "See you there!"

    def get_success_url(self):
        return reverse_lazy("workshop", args=(self.kwargs["slug"],))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workshops = models.Workshop.objects.filter(slug=self.kwargs["slug"])
        if not workshops:
            raise Http404()
        context["workshop"] = workshops.first()
        return context

    def form_valid(self, form):
        workshop = models.Workshop.objects.get(slug=self.kwargs["slug"])
        attendances = models.Attendance.objects.filter(
            email=form.cleaned_data["email"], workshop=workshop
        )
        if attendances:
            # RSVP for email + workshop already exists
            form.add_error("email", "Email already RSVPed for this workshop.")
            self.success_message = "Already RSVPed. Reminder sent!"
            obj = attendances.first()
        else:
            obj = form.save(commit=False)
            obj.workshop = workshop
            obj.save()

        mail.EmailMessage(
            subject=f"See you at: {obj.workshop.title}",
            body=utils.get_workshop_for_email(obj.workshop),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[obj.email],
            attachments=utils.get_email_attachments(obj.workshop.slug),
        ).send()
        mail_admins(
            f"RSVP <{obj.email}> for {obj.workshop.title}",
            f"**RSVP**\n\n<{obj.email}>" + f"\n\n**Workshop**\n\n{obj.workshop.title}",
        )
        return super().form_valid(form)


class BlogView(ListView):
    queryset = models.Post.objects.filter(published_at__isnull=False)
    template_name = "main/blog.html"


class PostView(DetailView):
    model = models.Post
    template_name = "main/post.html"


def subscribe(request):
    return render(request, "main/subscribe.html")


def unsubscribe_key(request, key):
    if models.Subscription.objects.filter(unsubscribe_key=key).exists():
        subscription = models.Subscription.objects.get(unsubscribe_key=key)
        email = subscription.email
        subscription.delete()
        messages.success(request, f"{email} deleted from mailing list.")
    else:
        messages.info(request, "Invalid link.")
    return redirect("index")


class SubmissionView(SuccessMessageMixin, FormView):
    form_class = forms.SubmissionForm
    template_name = "main/submit.html"
    success_url = reverse_lazy("index")
    success_message = "Thank you! We’ll be in touch :)"

    def form_valid(self, form):
        obj = form.save()
        mail_admins(
            f"New submission: {obj.submitter} <{obj.email}>",
            f"**Title**\n\n{obj.title}"
            + f"\n\n**Topic**\n\n{obj.topic}"
            + f"\n\n**Audience**\n\n{obj.audience}\n"
            + f"\n\n**Outcome**\n\n{obj.outcome}\n"
            + f"\n\n**When**\n\n{obj.when}\n"
            + f"\n\n**Links**\n\n{obj.links}\n",
        )
        return super().form_valid(form)


class FeedbackView(SuccessMessageMixin, FormView):
    form_class = forms.FeedbackForm
    template_name = "main/feedback.html"
    success_url = reverse_lazy("index")
    success_message = "Thank you 🙏"

    def form_valid(self, form):
        obj = form.save()
        mail_admins(
            f"New feedback: {obj.id}",
            f"**Comment**\n\n{obj.comment}",
        )
        return super().form_valid(form)


class ProposalView(SuccessMessageMixin, FormView):
    form_class = forms.ProposalForm
    template_name = "main/proposal.html"
    success_url = reverse_lazy("index")
    success_message = "Thanks—we might be in touch."

    def form_valid(self, form):
        obj = form.save()
        mail_admins(
            f"New proposal: {obj.email}",
            f"**Topic**\n\n{obj.topic}",
        )
        return super().form_valid(form)


class Broadcast(LoginRequiredMixin, FormView):
    form_class = forms.BroadcastForm
    template_name = "main/broadcast.html"
    success_url = reverse_lazy("broadcast")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dry_run_email"] = settings.EMAIL_BROADCAST_PREVIEW
        context["subscriptions_count"] = models.Subscription.objects.all().count()
        context["subscriptions_list"] = models.Subscription.objects.all().order_by(
            "created_at",
        )
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():

            # list of messages to sent out
            message_list = []
            record_ids = []

            # get all subscriptions
            subscription_list = models.Subscription.objects.all()
            # if dry run, override and sent only to broadcast preview email
            if form.cleaned_data.get("dry_run"):
                subscription_list = [
                    models.Subscription(email=settings.EMAIL_BROADCAST_PREVIEW)
                ]

            for subscription in subscription_list:
                unsubscribe_url = (
                    utils.get_protocol() + subscription.get_unsubscribe_url()
                )
                body = form.cleaned_data.get("body") + utils.get_email_body_footer(
                    unsubscribe_url
                )

                # initialise email record
                email_record = models.EmailRecord.objects.create(
                    email=subscription.email,
                    subject=form.cleaned_data.get("subject"),
                    body=body,
                    sent_at=None,
                )
                if not form.cleaned_data.get("dry_run"):
                    # in dry run case, there is no subscription object for the email record
                    # (there is a subscription but we create it temporarily and we don't save it)
                    email_record.subscription = subscription
                    email_record.save()
                record_ids.append(email_record.id)

                # create email message
                email = mail.EmailMessage(
                    subject=form.cleaned_data.get("subject"),
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscription.email],
                    reply_to=[settings.DEFAULT_FROM_EMAIL],
                    headers={
                        "X-PM-Message-Stream": settings.EMAIL_POSTMARK_HEADER,
                        "List-Unsubscribe": unsubscribe_url,
                        "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
                    },
                    attachments=utils.get_email_attachments(
                        form.cleaned_data.get("ics_attachment")
                    ),
                )
                message_list.append(email)

            # send out emails
            connection = mail.get_connection(
                "django.core.mail.backends.smtp.EmailBackend",
                # override email host because we use a different one for non-transactional emails
                host=settings.EMAIL_HOST_BROADCASTS,
            )
            connection.send_messages(message_list)
            models.EmailRecord.objects.filter(id__in=record_ids).update(
                sent_at=timezone.now()
            )
            messages.success(request, f"{len(message_list)} emails sent.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
