from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import StudyLog
from .models import Profile

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
class ProfileForm(forms.ModelForm):

    class Meta:
        model=Profile

        fields=[
            'bio',
            'avatar',
            'profile_picture',
            'github',
            'linkedin'
        ]
        widgets={
            'bio':forms.Textarea(attrs={
                'class':'form-control',
                'row':4
            }),
            'github': forms.URLInput(attrs={
                'class': 'form-control'
            }),

            'linkedin': forms.URLInput(attrs={
                'class': 'form-control'
            }),

        }
    # bio validation    

    def clean_bio(self):
        bio=self.cleaned_data.get('bio')

        if len(bio)<10:
            raise forms.ValidationError(
                "Bio must contain at least 10 characters."
            )
        return bio
    
    # Validate GitHub url

    def clean_github(self):
        github=self.cleaned_data.get('github')

        if github and "github.com" not in github:

            raise forms.ValidationError(
                "Enter a valid Github profile URL."
            )
        return github

    # validate linkedin URL

    def clean_linkedin(self):
        linkedin=self.cleaned_data.get('linkedin')

        if linkedin and "linkedin.com" not in linkedin:
            raise forms.ValidationError(
                "Enter a valid linkedin profile URL"
            )
        return linkedin
    

    # clean() which is used for multi-field validation it validates: relationship between fields , buisness rules and logic validation
    
    def clean(self):
        cleaned_data=super().clean()

        github=cleaned_data.get('github')

        linkedin=cleaned_data.get('linkedin')

        if github== linkedin and github!="":
            raise forms.ValidationError(
                "Github and linkedin links cannot be identical"
            )
        return cleaned_data
    