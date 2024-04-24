from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'description']  

    comments = forms.CharField(widget=forms.Textarea, required=False)

    def clean_description(self):
        description = self.cleaned_data.get('description', None)
        if not description:
            raise forms.ValidationError("Description field cannot be empty.")
        elif len(description) > 500:
            raise forms.ValidationError("Description must be at least 500 characters long.")
        return description