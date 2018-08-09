"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.8.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
HOST_DIR = "test"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR+"/packages")
sys.path.append(os.getcwd()+"/packages/mongo")
sys.path.append(BASE_DIR+"/packages/django")

sys.path.append(os.getcwd()+"/packages")

sys.path.append(os.getcwd()+"/packages/django")
from django.conf.urls import url, include

import quicky


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bw(lu4t*o&*ot4&gf^&74ksjz3r+ji6bxr_9$y0sacg*ks0m0w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','172.16.11.127']
# Application definition

INSTALLED_APPS = (
    'permission_backend_nonrel',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
AUTHENTICATION_BACKENDS = [
    'permission_backend_nonrel.backends.NonrelPermissionBackend',
    'quicky.backends.HashModelBackend'
]
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'django.middleware.security.SecurityMiddleware',
)



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
                'django.core.context_processors.csrf'
            ],
        },
    },
]
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES_ = {
   'default' : {
       'ENGINE': 'django_mongodb_engine',
       'NAME': 'lv01_lms',
       'HOST': '172.16.7.63',
       'PORT': 27017,
       'USER': 'sys',
       'PASSWORD': '123456'
   }

}
DATABASES = {
   'default' : {
       'ENGINE': 'django_mongodb_engine',
       'NAME': 'test',
       'HOST': 'localhost',
       'PORT': 27017,
       'USER': 'root',
       'PASSWORD': '123456'
   }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True

USE_MULTI_TENANCY=True
# MULTI_TENANCY_DEFAULT_SCHEMA="sys"
MULTI_TENANCY_DEFAULT_SCHEMA="hrm"
MULTI_TENANCY_CONFIGURATION=dict(
    host="localhost",
    port=27017,
    user="test",
    password="123456",
    name="hrm",
    collection="sys.customers"
)
MULTI_TENANCY_CONFIGURATION_=dict(
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456",
    name="lv01_lms",
    collection="sys.customers"
)
# import django_mongodb_engine.base
from quicky import backends
db_backend=dict(
    host="localhost",
    port=27017,
    user="root",
    password="123456",
    name="test",
    collection="sys.auth_token"
)
db_backend_=dict(
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456",
    name="lv01_lms",
    collection="sys.auth_token"
)
backends.set_config(db_backend)
from quicky import api


# api.connect(
#     host="172.16.7.63",
#     port=27017,
#     user="sys",
#     password="123456",
#     name="lv01_lms",
#     collection="sys_api_cache"
# )
api.connect(
    host="localhost",
    port=27017,
    user="root",
    password="123456",
    name="test",
    collection="sys.api_cache"
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
APPS=[
      # dict(host="admin",
      #      name="admin",
      #      path="apps/admin",
      #      # schema="lms"
      #      ),
      dict(host="sys",
           name="sys-admin",
           path="apps/sys_admin",
           schema="sys"),
      # dict(host="lms",
      #      name="lms",
      #      path="apps/lms"),
      #
      # dict(
      #     host="per", #"performance",
      #     name="performance",
      #     path="apps/performance",
      #     schema_delete="lacviet"
      # ),
      dict(host="",
           name="hrm",
           path="apps/hrm",
           schema="hrm",
           login="login",
           ),

      # dict(host="app-main",
      #      name="argo",
      #      path="apps/app_main",
      #      schema="lacviet")
]
aut_config_local=dict(
    provider="authorization.auth",
    name="test",
    host="localhost",
    port=27017,
    user="root",
    password="123456",
    schema="sys"
)
aut_config_local_=dict(
    provider="authorization.auth",
    name="lv01_lms",
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456",
    schema="sys"
)
quicky.authorize.set_config(aut_config_local)

language_config_local_=dict(
    provider="language_mongo_engine",
    name="lv01_lms",
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456",
    collection="sys_languages"
)
language_config_local=dict(
    provider="language_mongo_engine",
    name="test",
    host="localhost",
    port=27017,
    user="root",
    password="123456",
    collection="sys_languages"
)
quicky.language.set_config(language_config_local)

from qexcel import language
language.set_config(
    name="test",
    host="localhost",
    port=27017,
    user="root",
    password="123456",
    collection="sys.excel_languages"
)
# argo.language.load(language_congig_local)
# quicky.url.build_urls("apps",APPS)
AUTHORIZATION_ENGINE=quicky.authorize

LANGUAGE_ENGINE=quicky.language
LANGUAGE_CODE="en-us"

ROOT_URLCONF = 'apps'
quicky.url.build_urls(ROOT_URLCONF,APPS)

"""
setting database config for whole project.
use this syntax to get connection at any package:
from quicky import applications
then call applications.get_settings().database  
"""
from qmongo import  database as DB
main_db=dict(
    name="test",
    host="localhost",
    port=27017,
    user="root",
    password="123456"
)
main_db_=dict(
    name="lv01_lms",
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456"
)
database=DB.connect(main_db)
from quicky import encryptor
encryptor.set_config(
    host="localhost",
    port=27017,
    name="test",
    user="root",
    password="123456",
    collection="sys.encryptors")
import os
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.getcwd()+os.sep+ 'logs'+os.sep+'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
STATIC_ROOT = os.path.join(*(BASE_DIR.split(os.path.sep) + ['apps/static','apps/app_main/static']))