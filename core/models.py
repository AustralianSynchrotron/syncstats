import os
import sys

from core.settings import Settings
from django.conf import settings
from django.core.management import call_command


def init(search_path_list):
    # build list of available models
    model_list = []
    for search_path in search_path_list:
        if any("models.py" in fname for fname in os.listdir(search_path)):
            model_path = os.path.split(search_path)
            model_list.append(model_path[1])
            if not model_path[0] in sys.path:
                sys.path.append(model_path[0])

    # Allowed engine params: 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'
    settings.configure( DATABASES = {
                            'default': {
                                'ENGINE': 'django.db.backends.%s'%(Settings()['database']['backend']),
                                'NAME': Settings()['database']['name'],
                                'HOST': Settings()['database']['host'],
                                'PORT': Settings()['database']['port'],
                                'USER': Settings()['database']['username'],
                                'PASSWORD': Settings()['database']['password']
                            }
                        },
                        INSTALLED_APPS = model_list
                      )


def create():
    call_command('syncdb', verbosity=Settings()['server']['debug'], interactive=False)    
