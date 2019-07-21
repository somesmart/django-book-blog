from django.contrib import admin
from kbdb.models import *
from kbdb.forms import LessonRoundFormSet

class LessonRoundInline(admin.TabularInline):
	model = LessonRound
	extra = 3

class LessonAdmin(admin.ModelAdmin):
	inlines = [LessonRoundInline]	  

admin.site.register(RoundType)
admin.site.register(Round)
admin.site.register(LessonType)
admin.site.register(LessonRound)
admin.site.register(Lesson, LessonAdmin)