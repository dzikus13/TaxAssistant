from . import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'assistant',
        'USER': 'assistant',
        'PASSWORD': 'TaxAssistant123',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
