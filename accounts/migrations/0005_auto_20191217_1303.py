# Generated by Django 3.0 on 2019-12-17 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20191204_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(default='unknown_user', max_length=100),
        ),
    ]
