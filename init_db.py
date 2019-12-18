import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_lecture_manager.settings')
django.setup()

from accounts.models import Role

r = Role.objects.all()

r.create(name="학생")
r.create(name="교수")
