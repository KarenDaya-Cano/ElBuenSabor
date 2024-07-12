from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m=h@gk6wk$^4-qje5#0po*l7d)skgyedlqxm266wt$y2*o3mry'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#DEBUG = False # 27/06 modifique para mensajes de error

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

ALLOWED_HOSTS = []

#ALLOWED_HOSTS = ['*'] # 27/06 modifique para mensajes de error

MESSGES_STORAGE = "django.contrib.messages.storage.cookie.CooKieStorage"

STATICFILES_DIRS= ['C:/ElBuenSabor/ElBuenSabor/static/elbuensaborapp']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ElBuenSaborApp',
    'AdministrarApp',
    'CarritoApp', 
    'crispy_forms',
    'crispy_bootstrap5', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'ElBuenSabor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['C:/ElBuenSabor/ElBuenSaborApp/template/elbuensabor','C:/ElBuenSabor/AdministrarApp/template/administrar','C:/ElBuenSabor/CarritoApp/template/carrito','C:/ElBuenSabor/AdministrarApp/template/administrar/dashboard.html'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'CarritoApp.context_proccesor.total_carrito',
            ],
        },
    },
]

WSGI_APPLICATION = 'ElBuenSabor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'elbuensabor',
        'USER': 'sergio',
        'PASSWORD': '',
        'HOST': 'localhost',
        'POST':3306,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL='/imagen/'
MEDIA_ROOT='C:/ElBuenSabor/ElBuenSabor/static/elbuensaborapp/imagen/'

CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACK = 'bootstrap5'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'web.kmx3@gmail.com'
EMAIL_HOST_PASSWORD = 'ikss hwbz yxzl jybs'