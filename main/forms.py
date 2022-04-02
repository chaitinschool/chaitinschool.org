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


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = [
            "comment",
        ]


class ProposalForm(forms.ModelForm):
    class Meta:
        model = models.Proposal
        fields = [
            "email",
            "topic",
        ]


class BroadcastForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
    dry_run = forms.BooleanField(
        required=False, help_text="Send email only to preview user for testing."
    )

    def get_workshops_as_choices():
        workshops = [("no-ics", "NO ICS")]
        for workshop in models.Workshop.objects.filter(scheduled_at__isnull=False):
            workshops.append((workshop.slug, workshop.title))
        return workshops

    ics_attachment = forms.ChoiceField(
        choices=get_workshops_as_choices,
        label="Include ICS attachment",
    )


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = models.Attendance
        fields = ["email"]
