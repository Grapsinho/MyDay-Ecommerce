from pathlib import Path
# import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k@$fehltpvt(zmf)5q(l*m7u&p!9(!0mn7zhu%a%2i=h1y_-lm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["mydayecommerce.onrender.com", "localhost"]

import pymysql
pymysql.version_info = (1, 4, 6, 'final', 0)  # (major, minor, micro, releaselevel, serial)
pymysql.install_as_MySQLdb()

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    "mainApp.apps.MainappConfig",
    "inventory.apps.InventoryConfig",

    #api
    "rest_framework",
    'corsheaders',

    # External app
    "mptt",
    "channels",

    #Development
    # "debug_toolbar",
]

AUTH_USER_MODEL = 'inventory.Costumer'

CORS_ALLOW_ALL_ORIGINS = True

#შემიძლია მივუთითო რომელი ლინკები დაუშვას
# CORS_ALLOWED_ORIGINS = [
#     'http://127.0.0.1:5500',  # Your frontend URL
#     # Add other allowed origins as needed
# ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #api
    'corsheaders.middleware.CorsMiddleware',

    #debug-toolbar
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

REST_FRAMEWORK = {
    # და აქ ანუ ნებართვას ვაძლევთ მხოლოდ დარეგისტრირებულ იუზერებს
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',  # Adjust this URL as needed
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CACHE_TTL = 60 * 15  # Set cache timeout (e.g., 15 minutes)

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

ASGI_APPLICATION = 'core.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myday',
        'USER': 'root',
        'PASSWORD': 'chemirutpaswordi',
        'HOST': "localhost",
        'PORT': 3306  
    }
}

# DATABASES["default"] = dj_database_url.parse("postgres://mydayecommercedatabase_user:Qb3shtU6ErWIZnuctLKQlAtvBYvt4z77@dpg-clnjrhhll56s73fjbhb0-a.frankfurt-postgres.render.com/mydayecommercedatabase")

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_ROOT = BASE_DIR / 'static/images'
MEDIA_URL = 'images/'

STATIC_ROOT = "staticFiles"

# from mainApp import storage_config

# STATICFILES_STORAGE = storage_config.STORAGES['StaticFilesStorage']['BACKEND']

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# INTERNAL_IPS = [
#     "localhost",
# ]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}