# Generated by Django 2.0.4 on 2018-06-18 07:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20180516_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blocked',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]