from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from accounts.models import Profile, Role


class SignupForm(UserCreationForm):
    username = forms.EmailField(max_length=254, help_text='이메일로 가입가능합니다.', label="ID")

    name = forms.CharField(max_length=100, label='이름')
    id_number = forms.IntegerField(help_text='숫자로만 적어주세요.', label='직번/학번')
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label='신분', initial=0)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'role', 'id_number',)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "최소 8자 이상"


class UpdateUserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('id_number', 'name',)
    # TODO: 레이블 변경
