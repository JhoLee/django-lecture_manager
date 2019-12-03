from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    id_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default="unknown")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Reference: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Reference: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    """
    instance.profile.save()