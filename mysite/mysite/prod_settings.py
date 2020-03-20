import os
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ['CSX_SECRET_KEY']

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)