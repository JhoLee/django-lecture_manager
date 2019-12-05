from django.contrib.auth.views import PasswordChangeView
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.view_profile, name='view_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('password/', PasswordChangeView.as_view(success_url='accounts/profile',), name='password_change'),
    # toDO: Implement password changing...
]
