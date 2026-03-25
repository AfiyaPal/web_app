"""
Django settings for config project.

Created for development environment.
"""


from .base_settings import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'https://afiyapal.pythonanywhere.com/']


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#changed the initial configuration to use mysql for the database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Afiyapal_blogs',
        'USER': 'root',          # Using root for local dev is fine for now
        'PASSWORD': 'pass@sql', 
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_DIRS = [BASE_DIR / "static"]

