from django.contrib.auth.models import User
from django.shortcuts import render


def update_profile(request, user_id, **kwargs):
    """
    Reference: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    """
    user = User.objects.get(pk=user_id)

    if "name" in kwargs:
        user.profile.name = kwargs["name"]
    if "id_number" in kwargs:
        user.profile.id_number = kwargs["id_number"]
    if "role" in kwargs:
        user.profile.role = kwargs["role"]

    user.save()
