from django.contrib import admin

from .models import Course, Notice, Enrollment

admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Notice)
