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
        'reader',
		'started',
		'finished',
	)

class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        'edition',
        'quote_type',
        'reader',
    )

class RadarAdmin(admin.ModelAdmin):
    list_display = (
        'book',
    )    

class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'quote',
        'reader',
    )

admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Keyword)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Radar, RadarAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Shelf)
admin.site.register(ShelfDetail)
admin.site.register(QuoteType)