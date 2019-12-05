from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),  # TOdo: Change to custom login view
    path('logout/', views.signout, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('change-password/', auth_views.PasswordChangeView.as_view(success_url='accounts/profile', ), name='password_change'),
    # toDO: Implement password changing...
]
