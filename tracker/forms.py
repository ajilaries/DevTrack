from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import StudyLog


# Study Log Form

class StudyLogForm(forms.ModelForm):

    class Meta:

        model = StudyLog

        fields = ['hours', 'topic', 'notes']

        widgets = {

            'hours': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'topic': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'notes': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }
# Signup Form
class SignupForm(UserCreationForm):

    class Meta:
        model=User

        fields=[
            'username',
            'email',
            'password1',
            'password2'
        ]

     # email validation
    def clean_email(self):
        email=self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists"
            )
        return email
    
    def clean_username(self):
        username=self.cleaned_data.get(
            'username'
        )
        if len(username)<4:
            raise forms.ValidationError(
                "Username too short"
            )
        return username
    
def clean(self):

    cleaned_data = super().clean()

    password1 = cleaned_data.get(
        'password1'
    )

    username = cleaned_data.get(
        'username'
    )

    if password1 and username:

        if username.lower() in password1.lower():

            raise forms.ValidationError(
                "Password cannot contain username"
            )

    return cleaned_data
    
# UserCreationForm validates password, hashes password ,checks password match and validates usernames
