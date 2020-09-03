from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    email = forms.CharField(max_length=30, label='Email')

    def signup(self, request, user):
        user.email = self.cleaned_data['email']
        user.save()
        return user
