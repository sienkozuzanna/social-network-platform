from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from social_network.models import Post, Profile, Comment


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password",
        help_text="Password must meet the site-wide security requirements."
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    agree_to_terms = forms.BooleanField(required=True, label="I agree to the terms and conditions")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

    def clean_agree_to_terms(self):
        agree_to_terms = self.cleaned_data.get('agree_to_terms')
        if not agree_to_terms:
            raise forms.ValidationError("You must agree to the terms and conditions.")
        return agree_to_terms

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell something about yourself...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'accept': 'image/*'
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your post here...'}),
            'required': False,
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')

        if not content and not image:
            raise forms.ValidationError("You must provide either content or an image.")
        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Add a comment...',
                'class': 'form-control',
            }),
        }


