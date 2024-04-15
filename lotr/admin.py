from django.contrib import admin
from django.conf.urls import *
from django.http import HttpResponse
from lotr.models import *

class CharacterEventInline(admin.TabularInline):
	model = CharacterEvent
	extra = 5

class EventAdmin(admin.ModelAdmin):
	inlines = [CharacterEventInline]
	list_display = (
		'deck',
		'event_month',
		'event_day',
		'third_age_year',
	)

admin.site.register(Location)
admin.site.register(Journey)
admin.site.register(Event, EventAdmin)
admin.site.register(CharacterEvent)
admin.site.register(Character)
