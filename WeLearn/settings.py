import os
import json
import logging
import urllib.parse
from wechat_sdk import WechatConf

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configurations load from file
CONFIGS = json.loads(open(os.path.join(BASE_DIR, 'configs.json')).read())
for k, v in CONFIGS.items():
    try:
        exec('{} = {}'.format(k, v))
    except:
        exec('{} = "{}"'.format(k, v))

# Site and URL
SITE_DOMAIN = SITE_DOMAIN.rstrip('/')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

ALLOWED_HOSTS = ['*']

wechat_conf = WechatConf(
    token=WECHAT_TOKEN,
    appid=WECHAT_APPID,
    appsecret=WECHAT_SECRET,
    encrypt_mode=MSG_ENCRYPT,
    encoding_aes_key=WECHAT_AESKEY
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_mysql',
    'django_extensions',
    'djcelery',
    'wechat',
    'userpage',
    'homework',
    'notice',
    'team',
    'calendar_',
    'lecture'
]

if DEBUG:
    INSTALLED_APPS += ['django_nose']
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        '--with-coverage',
        '--cover-no-print',  # comment this line if confronted with bug
        # pip install git+https://github.com/nose-devs/nose@master --upgrade
        '--cover-erase',
        '--cover-html',
        '--cover-package=codex,homework,notice,userpage,wechat,WeLearn,ztylearn,team',
    ]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WeLearn.urls'

WSGI_APPLICATION = 'WeLearn.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


def get_url(path, params=None):
    full_path = urllib.parse.urljoin(SITE_DOMAIN, path)
    if params:
        return full_path + ('&' if urllib.parse.urlparse(full_path).query else '?') + urllib.parse.urlencode(params)
    else:
        return full_path


def get_redirect_url(path, params=None, scope='snsapi_base', state='view'):
    params = urllib.parse.urlencode([
        ('appid', WECHAT_APPID),
        ('redirect_uri', get_url(path, params)),
        ('response_type', 'code'),
        ('scope', scope),
        ('state', state)
    ])
    return 'https://open.weixin.qq.com/connect/oauth2/authorize?{}{}'.format(
        params, '#wechat_redirect'
    )

# Logging configurations
logging.basicConfig(
    format='%(levelname)-7s [%(asctime)s] %(module)s.%(funcName)s:%(lineno)d  %(message)s',
    level=logging.DEBUG if DEBUG else logging.WARNING,
)

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

import djcelery
djcelery.setup_loader()

from celery.schedules import crontab

CELERY_IMPORTS = ('WeLearn.tasks',)
CELERYBEAT_SCHEDULE = {
    'Mo Qunzhu': {
        'task': 'WeLearn.tasks.main',
        'schedule': 600,  # in seconds, or timedelta(seconds=10)
    },
    'Mo Qunzhu 2': {
        'task': 'userpage.tasks.notify',
        'schedule': crontab(minute=1, hour=0)
    },
}
CELERYD_TASK_SOFT_TIME_LIMIT = 120

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
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
            ],
        },
    },
]
