from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('id_number', 'name', 'role',)

    def __init__(self, *args, **kwargs):
        """
        Reference: https://stackoverflow.com/questions/16205908/django-modelform-not-required-field
        """
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['role'].requierd = False
