from django import forms
from django.db import transaction

from .models import NewsAndEvents, Session, Term, TERM


# news and events
class NewsAndEventsForm(forms.ModelForm):
    class Meta:
        model = NewsAndEvents
        fields = (
            "title",
            "summary",
            "posted_as",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["summary"].widget.attrs.update({"class": "form-control"})
        self.fields["posted_as"].widget.attrs.update({"class": "form-control"})


class SessionForm(forms.ModelForm):
    next_session_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                "type": "date",
            }
        ),
        required=True,
    )

    class Meta:
        model = Session
        fields = ["session", "is_current_session", "next_session_begins"]


class TermForm(forms.ModelForm):
    term = forms.CharField(
      widget=forms.Select(
            choices=TERM,
            attrs={
                "class": "browser-default custom-select",
            },
        ),
        label="Term",
    )
    is_current_term = forms.CharField(
        widget=forms.Select(
            choices=((True, "Yes"), (False, "No")),
            attrs={
                "class": "browser-default custom-select",
            },
        ),
        label="is current Term ?",
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "browser-default custom-select",
            }
        ),
        required=True,
    )

    next_term_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
        required=True,
    )

    class Meta:
        model = Term
        fields = ["term", "is_current_term", "session", "next_term_begins"]
