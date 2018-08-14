from django.contrib import admin
from django.conf.urls import *
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from ornaments.models import *

admin.site.register(Ornament)
admin.site.register(Giver)
admin.site.register(Receiver)