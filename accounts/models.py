from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(default="unknown_user", max_length=100)

    class Role(models.IntegerChoices):
        STUDENT = 0, '학생'
        PROFESSOR = 1, '교수'

    role = models.IntegerField(choices=Role.choices, default=0)

    # def __str__(self):
    #     return "{name}-{role}({id})".format(
    #         id=self.user.username,
    #         role=self.get_role_display(),
    #         name=self.name,
    #     )
    # def __str__(self):
    #     return "{role}/{id}/{name}-{user}".format(
    #         role=self.role,
    #         id=self.id_number,
    #         name=self.name,
    #         user=self.user,
    #     )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Reference: https://cjh5414.github.io/extending-user-model-using-one-to-one-link/
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Reference: https://cjh5414.github.io/extending-user-model-using-one-to-one-link/
    """
    instance.profile.save()
