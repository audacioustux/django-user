# Generated by Django 2.0.4 on 2018-06-18 11:37

import django.core.validators
from django.db import migrations, models
import user.validator


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20180618_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 40 characters or fewer. Letters, digits and .-_ only.', max_length=45, unique=True, validators=[user.validator.validate_check_blacklist, django.core.validators.RegexValidator(regex='^(?=.{3,50}$)(?![_.])(?!.*[_.]{2})(?=.*[a-z])[a-z0-9._]+(?<![_.])$')], verbose_name='username'),
        ),
    ]