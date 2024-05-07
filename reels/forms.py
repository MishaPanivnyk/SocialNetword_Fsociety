from django import forms
from .models import Reel

class ReelForm(forms.ModelForm):
    class Meta:
        model = Reel
        fields = ['video', 'description']

    comments = forms.CharField(widget=forms.Textarea, required=False)

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 500:
            raise forms.ValidationError("Description must be at most 500 characters long.")
        return description