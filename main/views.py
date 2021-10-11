from django.contrib import messages
from django.shortcuts import render

from main import forms


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
        # submitter_email = form.cleaned_data["email"]
        # mail_admins(
        #    f"New subscription: {submitter_email}",
        #    f"Someone new has subscribed to Sci-Hub London. Hooray!\n\nIt's {submitter_email}\n",
        # )

        messages.success(request, "Thanks! Email saved—we’ll be in touch soon!")
        return render(request, "main/index.html")
