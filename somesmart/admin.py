from django.contrib import admin
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from sssd.somesmart.models import *
from tagging.forms import TagField
from zinnia.models import Entry
from zinnia.admin import EntryAdmin

class EditionInline(admin.TabularInline):
    model = Edition
    extra = 3

class BookAdmin(admin.ModelAdmin):
    inlines = [EditionInline]  
    list_display = (
        'title',
        'author',
        'genre',
    )
    
    list_filter = ('genre',)

class ReviewAdmin(admin.ModelAdmin):
	list_display = (
		'edition',
		'started',
		'finished',
	)    

admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Keyword)
admin.site.register(Quote)
admin.site.register(Radar)
admin.site.register(Note)
admin.site.register(Shelf)
admin.site.register(ShelfDetail)
admin.site.register(QuoteType)