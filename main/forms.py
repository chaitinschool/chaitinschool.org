from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjUserCreationForm
from django.core import validators as dj_validators

from main import models


class UserCreationForm(DjUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]


class UserAvatarForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(),
        validators=[dj_validators.FileExtensionValidator(["jpeg", "jpg", "png"])],
    )


class UserAvatarRemoveForm(forms.Form):
    """Remove user's avatar fields."""


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = models.Subscription
        fields = ["email"]


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


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadImagesForm(forms.Form):
    file = MultipleFileField(
        validators=[
            dj_validators.FileExtensionValidator(
                ["jpeg", "jpg", "png", "svg", "gif", "webp"]
            )
        ],
    )
