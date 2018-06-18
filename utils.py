from django.utils.crypto import get_random_string


def generate_activation_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^*(-_=+)'
    secret_key = get_random_string(256, chars)
    return secret_key
