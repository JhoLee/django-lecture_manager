# Generated by Django 3.0 on 2019-12-17 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lecture', '0003_auto_20191217_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.IntegerField(choices=[(1, '1학기'), (2, '2학기'), (3, '여름학기'), (4, '겨울학')]),
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('attachment', models.FileField(upload_to='uploads/None/notice/')),
                ('pub_dt', models.DateTimeField(auto_now_add=True)),
                ('edit_dt', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.Course')),
                ('publisher', models.ForeignKey(default='unknown user', on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
