from django.contrib import messages
from django.contrib.auth import forms as auth_forms, update_session_auth_hash
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.forms import SignupForm, UpdateUserProfileForm, SigninForm, ChangePasswordForm
from django_lecture_manager import settings


def signin(request):
    if request.user.is_authenticated:
        messages.error(request, "이미 로그인 됨")
        context = {}
        return redirect('accounts:view_profile')
    if request.method == "POST":
        form = SigninForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, user.profile.name + "님, 환영합니다.")
            return redirect('accounts:view_profile')

        else:
            messages.error(request, '로그인 실패...')
    else:
        form = SigninForm()
    context = {
        "login_form": form,
    }
    return render(request, 'accounts/login.html', context=context)


def signout(request):
    logout(request)
    return redirect('accounts:login')


def signup(request):
    """
    회원가입을 위한 뷰.
    Login 되어 있을 시에는 회원가입 페이지에 접근하지 못하도록 함.
    """
    if request.user.is_authenticated:
        messages.error(request, "이미 로그인 됨")
        context = {}
        return render(request, 'global/error_page.html', context=context)
    else:
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()

                # set profile data
                profile = user.profile
                profile.name = form.cleaned_data.get('name')
                profile.id_number = form.cleaned_data.get('id_number')
                profile.role = form.cleaned_data.get('role')
                form.save()

                username = form.cleaned_data.get('username')
                raw_pass = form.cleaned_data.get('password1')

                user = authenticate(request, username=username, password=raw_pass)
                login(request, user, )
                return redirect('accounts:view_profile')
            else:
                messages.error(request, "회원가입 실패!")
        else:
            form = SignupForm()
        context = {
            "user_form": form,
            "user": request.user,
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
        uri = '{login_url}?next={redirect_to}'.format(
            login_url=settings.LOGIN_URL,
            redirect_to=request.path
        )

        return redirect(uri)
    return render(request, 'accounts/profile_view.html', context=context)


def update_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "로그인 하셔야 합니다.")
        context = {}
        return redirect('accounts:login')
    else:
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


def change_password(request):
    # todo: Custom password change form's style
    if not request.user.is_authenticated:
        messages.error(request, "로그인 하셔야 합니다.")
        context = {}
        return redirect('accounts:login')
    else:
        if request.method == "POST":
            change_password_form = ChangePasswordForm(request.user, request.POST)

            if change_password_form.is_valid():
                user = change_password_form.save()
                update_session_auth_hash(request, user)
                messages.info(request, '비밀번호 변경 완료')

                return redirect('accounts:view_profile')
            else:
                messages.error(request, '비밀번호 변경 실패')

        else:
            change_password_form = ChangePasswordForm(request.user)
            context = {
                'password_change_form': change_password_form,
            }

        return render(request, 'accounts/password_change.html', context=context)
