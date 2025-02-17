from datetime import timedelta
import os
from pathlib import Path
import ssl 
from django.urls import path
import cloudinary
import environ
import dj_database_url
import pymysql

pymysql.install_as_MySQLdb()

# env = environ.Env(
#     # set casting, default value
#     DEBUG=(bool, True)
# )
# reading .env file
environ.Env.read_env()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-2bqb=k6iq^6kyeykco4(@!uy2yk-)4s=^93dk6=rsyenbj_x=)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = ['https://socialnetword-fsociety.onrender.com','socialnetword-fsociety.onrender.com', 'localhost', '0.0.0.0','127.0.0.1','https://127.0.0.1','https://f6e2-46-219-135-16.ngrok-free.app']
ALLOWED_HOSTS = ['*']
#авторизація
AUTH_USER_MODEL = 'account.CustomUser'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME' : timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME' : timedelta(days=180),
    'ROTATE_REFRESH_TOKENS' : False,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}


DJOSER = {
    'LOGIN_FIELD': 'email',
    'PASSWORD_RESET_CONFIRM_URL': '/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'LOGOUT_ON_PASSWORD_CHANGE': True,
    'SERIALIZERS': {},
}

CORS_ORIGIN_ALLOW_ALL = True
#CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'https://oleksandrkuchera.github.io',
   "http://127.0.0.1:5173",
   "http://127.0.0.1:6379",
   "https://f6e2-46-219-135-16.ngrok-free.app",
]

#CSRF_TRUSTED_ORIGINS = [
#    "http://127.0.0.1:5173",
#]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
    'corsheaders',
    #'channels',
    #'channels_redis',
    'account',
    'friend',
    'chat',
    'posts',
    'reels',
    #'player',
    'stories',
    'group',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware', захист CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'F_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'F_backend.wsgi.application'

#Data Base
# DATABASES = {
#     "default": {
#         'ENGINE': 'django.db.backends.postgresql',
#         "NAME": env('DB_NAME'),
#         "USER": env('DB_USER'),
#         "PASSWORD": env('DB_PASSWORD'),
#         "HOST": env('DB_HOST'),
#         "PORT": env('DB_PORT'),
#     }
# }

# DATABASES = {
#     "default": {
#         'ENGINE': env('ENGINE1'),
#         "NAME": env('DB_NAME1'),
#         "USER": env('DB_USER1'),
#         "PASSWORD": env('DB_PASSWORD1'),
#         "HOST": env('DB_HOST1'),
#         "PORT": env('DB_PORT1'),
#     }
# }

DATABASES = {
    'default': dj_database_url.parse(
        'postgres://avnadmin:AVNS_0rimo2r7_vfOHHrxTQn@agreggator-stream24chasa-ccb3.b.aivencloud.com:13448/fsociety?sslmode=require'
    )
}
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
MEDIA_URLS ='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


#Веріф на пошту
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'leato4ek@gmail.com'
EMAIL_HOST_PASSWORD = 'oofhhjiyvkghjcjp'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
#EMAIL_USE_SSL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#cloudinary Зберігає пости

cloudinary.config( 
  cloud_name = "dfdomeztp", 
  api_key = "157137124786164", 
  api_secret = "tu3mecsJLc0P8RAEZCBNOv2TmtQ" 
)
#6379
#CHANNEL_LAYERS = {
#    'default': {
#        'BACKEND': 'channels_redis.core.RedisChannelLayer',
#        'CONFIG': {
#            'hosts': [('127.0.0.1', 6379)],
#        },
#    },
#}

#CHANNELS_WS_PROTOCOLS = ["ws", "wss"]
#CHANNELS_WS_ALLOWED_ORIGINS = [
#    "http://localhost:5173/",
#]


SESSION_COOKIE_AGE = 900  
