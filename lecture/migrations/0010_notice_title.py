# Generated by Django 3.0 on 2019-12-17 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0009_auto_20191217_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='title',
            field=models.CharField(default='Test Notice', max_length=200),
            preserve_default=False,
        ),
    ]
