from django import forms
from django.contrib.auth.models import User
from authentication.models import Profile


class UserForm(forms.ModelForm):
    model = User
    fields = ('first_name', 'last_name')
