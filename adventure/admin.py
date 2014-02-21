from django.contrib import admin
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from sssd.adventure.models import *

class WordInline(admin.TabularInline):
    model = Word
    extra = 3

class WordGroupAdmin(admin.ModelAdmin):
    inlines = [WordInline]      

class StoryAdmin(admin.ModelAdmin):
    list_display = (
        'level',
        'character',
        'wordgroup',
        'next_level',
    )

admin.site.register(Game)
admin.site.register(Character)
admin.site.register(Level)
admin.site.register(LevelCharacter)
admin.site.register(WordGroup, WordGroupAdmin)
admin.site.register(Word)
admin.site.register(Story, StoryAdmin)
admin.site.register(Unknown)