from django.contrib import messages
from django.core.mail import mail_admins
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from main import forms, models


def index(request):
    if request.method == "GET" or request.method == "HEAD":
        return render(
            request,
            "main/index.html",
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


def workshops(request):
    return render(request, "main/workshop.html")


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
