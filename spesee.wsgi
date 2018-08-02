import os
import sys

path='/home/somesmart'

if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'nature.spesee_settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
