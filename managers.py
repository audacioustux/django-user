from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db import transaction
from .utils import generate_activation_key
from django.db.models import Q
import hashlib
from django.utils.timezone import now
from smtplib import SMTPException
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist, ValidationError, NON_FIELD_ERRORS
from django.contrib.auth import password_validation
from django.utils.crypto import get_random_string
import string
# TODO: clean this massy imports


class EmailActivationManager(models.Manager):
    def create_key(self, instance):  # user instance passed in
        key = generate_activation_key()
        key_instance = self.model(
            user=instance,
            email=instance.email,
            key=key,
        )
        try:
            instance.email_user(
                subject="activation code",
                message=key+'&'+instance.email
            )
        except SMTPException:
            pass
        # TODO: send error to api payload
        else:
            key_instance.last_sent_mail = now()

        key_instance.save()
        return key_instance

    def refresh_key(self):
        pass

    def verify_key(self, key, email):
        try:
            key_entry = self.get(email=email, key=key)
        except ObjectDoesNotExist:
            print("wrong key")
            # TODO: send error to api payload
        else:
            if not key_entry.is_expired():
                key_entry.verified = True
                key_entry.save()
                key_entry.user.objects.make_active()
                return email


class UserManager(BaseUserManager):
    def create_user(self, full_name, password, email, username=None, clean=True):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            is_active=True
        )
        if not username:
            prefix = 'nbid_'
            length = 45
            allowed_chars = string.ascii_lowercase + string.digits
            _username = prefix + get_random_string(length - len(prefix), allowed_chars)
            user.username = _username
            # TODO: check in manager for unique error
        else:
            user.username = self.model.normalize_username(username)

        user.set_password(password)

        if clean is False:
            user.save()
            return user
        else:
            try:
                user.full_clean()
            except ValidationError as e:
                raise e
            else:
                user.save()
                return user

    def create_superuser(self, email, full_name, password, username):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            full_name,
            password,
            username,
            clean=False
        )
        user.is_active = True
        user.is_admin = True
        user.save()
        return user

    def make_active(self, active):
        user = self.model(
            is_active=active
        )
        user.save()
        return user.is_active

