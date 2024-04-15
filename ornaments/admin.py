from django.contrib import admin
from django.conf.urls import *
from django.http import HttpResponse
from ornaments.models import *

admin.site.register(Ornament)
admin.site.register(Giver)
admin.site.register(Receiver)
