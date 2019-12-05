import django.contrib.auth.forms as auth_forms
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from accounts.models import Profile, Role


class SignupForm(auth_forms.UserCreationForm):
    username = forms.EmailField(max_length=254, help_text='이메일로 가입가능합니다.', label="ID")

    name = forms.CharField(max_length=100, label='이름')
    id_number = forms.IntegerField(help_text='숫자로만 적어주세요.', label='직번/학번')
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label='신분', initial=0)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'role', 'id_number',)

    def __init__(self, *args, **kwargs):
        super(auth_forms.UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "최소 8자 이상"

        # form-control
        # Ref. https://stackoverflow.com/questions/31627253/django-modelform-with-bootstrap
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class SigninForm(auth_forms.AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

    # form=control
    # Ref. https://stackoverflow.com/questions/31627253/django-modelform-with-bootstrap
    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class UpdateUserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('id_number', 'name',)

    def __init__(self, *args, **kwargs):
        super(UpdateUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['id_number'].label = "직번/학번"
        self.fields['name'].label = "이름"

        # form-control
        # Ref. https://stackoverflow.com/questions/31627253/django-modelform-with-bootstrap
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
