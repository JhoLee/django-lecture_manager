from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.forms import SignupForm, UpdateUserProfileForm


def signup(request):
    """
    회원가입을 위한 뷰.
    Login 되어 있을 시에는 회원가입 페이지에 접근하지 못하도록 함.
    """
    error_message = ""
    if request.user.is_authenticated:
        error_message = "(대충 로그인되어 있다는 메세지)"
        context = {
            "error_message": error_message
        }
        return render(request, 'global/error_page.html', context=context)
    else:
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                print("valid")
                user = form.save()
                user.refresh_from_db()
                user.profile.id_number = form.cleaned_data.get('id_number')
                user.role = form.cleaned_data.get('role')
                user.save()

                user = authenticate(username=user.username, password=form.cleaned_data.get('password,1'))
                login(request, user)
                return redirect('accounts:profile')
            else:
                error_message = "(대충 에러가 있다는 메세지)"
        else:
            form = SignupForm()
        context = {
            "user_form": form,
            "error_message": error_message,
        }

        return render(request, 'accounts/signup.html', context=context)


def view_profile(request):
    if request.user.is_authenticated:
        user = {
            'username': request.user.username,
            'name': request.user.profile.name,
            'role': request.user.profile.role,
            'id_number': request.user.profile.id_number
        }

        context = {
            'user': user,
        }
    else:
        redirect('accounts:singup')
    return render(request, 'accounts/profile_view.html', context=context)


@login_required
def update_profile(request):
    # TOdo: Add password validation
    user = request.user
    profile = user.profile
    initial_data = {
        'name': profile.name,
        'role': profile.role,
        'id_number': profile.id_number,
    }
    user_update_form = UpdateUserProfileForm(request.POST or None, initial=initial_data, instance=profile)
    if request.method == 'POST':
        if user_update_form.is_valid():
            profile = user_update_form.save(commit=False)

            profile.save()
            return HttpResponseRedirect(reverse('accounts:view_profile'))

    context = {
        'user_update_form': user_update_form,
    }
    return render(request, 'accounts/profile_update.html', context)
