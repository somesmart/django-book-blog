from django.contrib import admin
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from sssd.adventure.models import *

admin.site.register(Game)
admin.site.register(Character)
admin.site.register(Level)
admin.site.register(LevelCharacter)
admin.site.register(WordGroup)
admin.site.register(Word)
admin.site.register(Story)
admin.site.register(Unknown)