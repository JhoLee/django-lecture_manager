import django.contrib.auth.forms as auth_forms
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from accounts.models import Profile


class SignupForm(auth_forms.UserCreationForm):
    username = forms.EmailField(max_length=254, help_text='이메일 가입만 가능합니다.', label="ID")

    name = forms.CharField(help_text='실명으로 적어주세요.', max_length=100, label='이름')
    id_number = forms.IntegerField(help_text='숫자로만 적어주세요.', label='직번/학번')

    ROLE_CHOICES = (
        ("0", '학생'),
        ('1', '교수'),
    )
    role = forms.ChoiceField(help_text='선택해주세요.', choices=ROLE_CHOICES, label='신분', initial=0)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'id_number', 'role',)

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


class ChangePasswordForm(auth_forms.PasswordChangeForm):
    # form=control
    # Ref. https://stackoverflow.com/questions/31627253/django-modelform-with-bootstrap
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
