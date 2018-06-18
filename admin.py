from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import EmailActivation

user = get_user_model()
# Register your models here.
admin.site.register(user)
admin.site.register(EmailActivation)