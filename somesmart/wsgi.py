#!/home/mission/mydjango/bin/python

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "somesmart.settings")

application = get_wsgi_application()
