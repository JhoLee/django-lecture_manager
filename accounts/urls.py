from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('update_profile/', views.update_profile, name='update_profile'),

]
