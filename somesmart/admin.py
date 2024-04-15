from django.contrib import admin
from django.conf.urls import *
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from somesmart.models import *
from tagging.forms import TagField
# from zinnia.models import Entry
# from zinnia.admin import EntryAdmin
from django.contrib import admin
import nested_admin

class QuoteInline(nested_admin.NestedTabularInline):
	model = Quote
	extra = 5

class ReveiwInline(nested_admin.NestedTabularInline):
	model = Review
	extra = 1

class EditionInline(nested_admin.NestedTabularInline):
	model = Edition
	extra = 1
	inlines = [QuoteInline, ReveiwInline]

class SeriesInline(nested_admin.NestedTabularInline):
	model = SeriesDetail
	extra = 1

class RadarInline(nested_admin.NestedTabularInline):
	model = Radar
	extra = 1

class FavoriteInline(nested_admin.NestedTabularInline):
	model = Favorite
	extra = 1

class BookAdmin(nested_admin.NestedModelAdmin):
	inlines = [EditionInline, SeriesInline, RadarInline, FavoriteInline]
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

class ListDetailInline(admin.TabularInline):
	model = ListDetail
	extra = 3

class ListAdmin(admin.ModelAdmin):
	inlines = [ListDetailInline]
	list_display = (
		'list_name',
		'list_descr',
	)

class FavoriteAdmin(admin.ModelAdmin):
	list_display = (
		'book',
		'user',
		'rank',
	)

class SeriesAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'count'
	)

class AuthorAdmin(admin.ModelAdmin):
    ordering = ['last_name', 'first_name']


admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Genre)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Keyword)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Radar, RadarAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Shelf)
admin.site.register(ShelfDetail)
admin.site.register(QuoteType)
admin.site.register(List, ListAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Series, SeriesAdmin)
