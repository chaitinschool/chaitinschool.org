from django import forms

from main import models


    class Meta:


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = models.Subscription
        fields = ["email"]


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = [
            "comment",
        ]


class BroadcastForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
    dry_run = forms.BooleanField(
        required=False, help_text="Send email only to preview users for testing."
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


class AnnounceForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
    dry_run = forms.BooleanField(
        required=False, help_text="Send email only to preview users for testing."
    )
