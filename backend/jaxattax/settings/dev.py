from jaxattax.settings.base import *

LOCAL_BASE = BASE_DIR / "local"

ASSETS_BASE = LOCAL_BASE / "assets"
STATIC_BASE = ASSETS_BASE / "static"
MEDIA_BASE = ASSETS_BASE / "media"

STATICFILES_DIRS = ['/opt/frontend/dist']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'database',
        'NAME': 'jaxattax',
        'USER': 'jaxattax',
        'PASSWORD': 'dev-password',
    }
}

SECRET_KEY = 'shhh not very secret'
