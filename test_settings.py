from testapp.settings import *  # noqa
from testapp.settings.base import INSTALLED_APPS as TESTAPP_INSTALLED_APPS
from testapp.settings.base import MIDDLEWARE_CLASSES as TESTAPP_MIDDLEWARE_CLASSES
from os.path import abspath, dirname, join

PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testapp_test.db'
    }
}

DEBUG = True
CELERY_ALWAYS_EAGER = True

DEFAULT_SITE_PORT = 8000

INSTALLED_APPS = TESTAPP_INSTALLED_APPS + [
    'secretballot',
    'likes'
]

MIDDLEWARE_CLASSES = TESTAPP_MIDDLEWARE_CLASSES + [
    'likes.middleware.SecretBallotUserIpUseragentMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(PROJECT_ROOT, 'testapp', 'templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'molo.core.context_processors.locale',
                'molo.core.processors.compress_settings',
                'wagtail.contrib.settings.context_processors.settings',
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "mote.loaders.app_directories.Loader",
                "django.template.loaders.app_directories.Loader",
            ]
        },
    },
]
