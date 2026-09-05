from django import forms
from .models import Inquiry


class InquiryForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Inquiry
        fields = ["name", "email", "company", "service", "budget", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value
