from django.contrib import admin
from django.conf.urls import *
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from adventure.models import *
from adventure.forms import StoryDetailFormset, LevelCharacterFormset

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

class StoryInline(admin.TabularInline):
	model = Story
	formset = StoryDetailFormset
	extra = 0
	fk_name = "level"

class LevelCharacterInline(admin.TabularInline):
	model = LevelCharacter
	formset = LevelCharacterFormset
	extra = 0

class LevelAdmin(admin.ModelAdmin):
	inlines = [StoryInline, LevelCharacterInline]
	list_display = (
		'game',
		'level_descr',
	)

	list_filter = ('game',)
	ordering = ('game', 'level_descr')

class UnknownAdmin(admin.ModelAdmin):
	list_display = (
		'game',
		'level',
		'term',
		'attempts',
	)

class WordAdmin(admin.ModelAdmin):
	list_display = (
		'word_descr',
		'wordgroup',
		'game',
	)

	list_filter = ('game',)

class GenericAdmin(admin.ModelAdmin):
	list_display = (
		'game',
		'wordgroup',
	)

	list_filter = ('game',)

admin.site.register(Game)
admin.site.register(Character)
admin.site.register(Level, LevelAdmin)
admin.site.register(LevelCharacter)
admin.site.register(WordGroup, WordGroupAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Unknown, UnknownAdmin)
admin.site.register(Generic, GenericAdmin)
