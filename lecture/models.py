import os

from django.db import models
from django.dispatch import receiver

from accounts.models import User


class Course(models.Model):
    name = models.CharField(max_length=100)

    class Semester(models.IntegerChoices):
        FIRST = 1, '1학기'
        SECOND = 2, '2학기'
        THIRD = 3, '여름학기'
        FOURTH = 4, '겨울학기'

    semester = models.IntegerField(choices=Semester.choices)
    year = models.IntegerField()
    description = models.TextField()
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    open_dt = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{id}_{year}_{semester}_{name}".format(
            id=self.id,
            year=self.year,
            semester=self.semester,
            name=self.name
        )


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    join_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{course}: {student}".format(
            course=self.course.name,
            student=self.student.profile.name,
        )


def notice_upload_path(self, filename):
    return 'uploads/{0}/notice/{1}/'.format(self.course.name, filename)


class Notice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    publisher = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='unknown user')
    title = models.CharField(max_length=200)
    content = models.TextField()
    file = models.FileField(
        upload_to=notice_upload_path,
        blank=True,
        null=True

    )
    pub_dt = models.DateTimeField(auto_now_add=True)
    edit_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{course_name}-{publisher_name}-{title}-{pub_dt}".format(
            course_name=self.course.name,
            publisher_name=self.publisher.profile.name,
            title=self.title,
            pub_dt=self.pub_dt,

        )


@receiver(models.signals.post_delete, sender=Notice)
def auto_delete_on_delete_notice(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Notice)
def auto_delete_on_change_notice(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
