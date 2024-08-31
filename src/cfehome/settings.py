"""
Django settings for cfehome project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# for gmail configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com", cast=str)
EMAIL_PORT = config("EMAIL_PORT", cast=str, default="587")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str, default=None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str, default=None)


ADMINS = [("Kartikey", "kartikey.23558@sscbs.du.ac.in")]
MANAGERS = ADMINS

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = str(os.environ.get("DJANGO_DEBUG")).lower() == "true"
DEBUG = config("DJANGO_DEBUG", cast=bool)

print("DEBUG", DEBUG, type(DEBUG))

ALLOWED_HOSTS = [".railway.app"]  # https://saas.prod.railway.app
if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    # django-apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # my-apps
    "visits",
    "commando",
    "profiles",
    "subscriptions",
    # Third party packages (apps)
    "allauth_ui",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "widget_tweaks",
    "slippers",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cfehome.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cfehome.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CONN_MAX_AGE = config("CONN_MAX_AGE", cast=int)
DATABASE_URL = config("DATABASE_URL", cast=str)

if DATABASE_URL is not None:
    from dj_database_url import config as dj_config

    DATABASES = {
        "default": dj_config(
            default=DATABASE_URL, conn_health_checks=True, conn_max_age=CONN_MAX_AGE
        )
    }
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Allauth config

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
LOGIN_REDIRECT_URL = "/"
ALLAUTH_UI_THEME = "light"
# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

SOCIALACCOUNT_PROVIDERS = {"github": {"VERIFIED_EMAIL": True}}

STATIC_URL = "static/"


STATICFILES_BASE_DIR = BASE_DIR / "staticfiles"
STATICFILES_VENDOR_DIR = STATICFILES_BASE_DIR / "vendors"

# this is the place where django will look for source of static files, including vendor css and js
STATICFILES_DIRS = [
    STATICFILES_BASE_DIR,
]

# output of python manage.py collectstatic, means django will collect static file from STATICFILES_DIR and store it in organised manner in below location

STATIC_ROOT = BASE_DIR / "local-cdn"

if not DEBUG:
    STATIC_ROOT = BASE_DIR / "prod-cdn"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
