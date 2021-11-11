from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import mail_admins
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from main import forms, models


def index(request):
    if request.method == "GET" or request.method == "HEAD":
        next_workshop = None
        if models.Workshop.objects.exists():
            next_workshop = (
                models.Workshop.objects.all().order_by("-transpired_at").first()
            )
        return render(
            request,
            "main/index.html",
            {
                "next_workshop": next_workshop,
            },
        )

    elif request.method == "POST":
        form = forms.SubscriptionForm(request.POST)

        # if not valid
        if not form.is_valid():
            if "email" in form.errors and form.errors["email"] == [
                "Subscription with this Email already exists."
            ]:
                # if case of already subscribed
                messages.info(request, "Email already subscribed :)")
                return render(
                    request,
                    "main/index.html",
                )

            else:
                # all other cases
                messages.error(
                    request,
                    "Well, that didn't work :/",
                )
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
            "Someone new has subscribed to the Chaitin School list. Hooray!\n"
            + f"\nIt's {submitter_email}\n",
        )

        messages.success(request, "Thanks! Email saved—we’ll be in touch soon!")
        return render(request, "main/index.html")


class WorkshopDetailView(DetailView):
    model = models.Workshop


class BlogView(ListView):
    model = models.Post
    template_name = "main/blog.html"


class PostView(DetailView):
    model = models.Post
    template_name = "main/post.html"


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
