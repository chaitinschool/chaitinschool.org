from django import forms

from main import models


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = models.Subscription
        fields = ["email"]


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = models.Submission
        fields = [
            "submitter",
            "email",
            "links",
            "title",
            "topic",
            "audience",
            "outcome",
            "when",
        ]
        widgets = {
            "links": forms.Textarea(attrs={"rows": 2}),
            "topic": forms.Textarea(attrs={"rows": 5}),
            "audience": forms.Textarea(attrs={"rows": 3}),
            "outcome": forms.Textarea(attrs={"rows": 4}),
            "when": forms.TextInput,
        }


class RequestForm(forms.ModelForm):
    class Meta:
        model = models.Request
        fields = [
            "email",
            "topic",
        ]
