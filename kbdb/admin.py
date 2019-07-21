from django.contrib import admin
from kbdb.models import *
from kbdb.forms import LessonRoundFormSet
from markdownx.admin import MarkdownxModelAdmin

class LessonRoundInline(admin.TabularInline):
	model = LessonRound
	extra = 12

class LessonAdmin(admin.ModelAdmin):
	inlines = [LessonRoundInline]	  

admin.site.register(RoundType)
admin.site.register(Round, MarkdownxModelAdmin)
admin.site.register(LessonType)
admin.site.register(LessonRound)
admin.site.register(Lesson, LessonAdmin)