from django import forms

from .models import JobDescription


class JobDescriptionForm(forms.ModelForm):

    class Meta:

        model = JobDescription

        fields = [
            "role",
            "company",
            "description",
        ]

        widgets = {

            "description": forms.Textarea(
                attrs={
                    "rows": 10
                }
            )
        }