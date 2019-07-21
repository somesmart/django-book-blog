from django.db import models
from django.urls import reverse
import datetime
from django.contrib.auth import get_user_model
import os
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from tagging.registry import register

class IntegerRangeField(models.IntegerField):
	def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
		self.min_value, self.max_value = min_value, max_value
		models.IntegerField.__init__(self, verbose_name, name, **kwargs)
	def formfield(self, **kwargs):
		defaults = {'min_value': self.min_value, 'max_value':self.max_value}
		defaults.update(kwargs)
		return super(IntegerRangeField, self).formfield(**defaults)

class Genre(models.Model):
	name = models.TextField(max_length=100)
	slug = models.SlugField()

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			# Newly created object, so set slug
			self.slug = slugify(self.name)

		super(Genre, self).save(*args, **kwargs)

class Author(models.Model):
	last_name = models.CharField(max_length=200)
	first_name = models.CharField(max_length=200)
	birth_date = models.DateTimeField(null=True, default=None, blank=True)
	death_date = models.DateTimeField(null=True, default=None, blank=True)
	pen_name = models.BooleanField()
	parent_author = models.ForeignKey('self', blank=True, default=None, null=True, help_text='The real name of a pen name', on_delete=models.CASCADE)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)	

class Book(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	original_publication = models.DateTimeField()
	synopsis = models.TextField(blank=True)
	reading_age = models.IntegerField()
	content_advisory = models.TextField(blank=True)
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

class Edition(models.Model):
	def get_image_path(instance, filename):
		return os.path.join('photos/book', str(instance.book.id), filename)

	FORMAT = (
		(1, 'Hardcover'),
		(2, 'Paperback'),
		(3, 'Digital'),
		(4, 'Audio'),
	)

	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	isbn = models.CharField(max_length=20)
	published = models.DateTimeField()
	pages = models.IntegerField()
	format = models.IntegerField(choices=FORMAT)
	cover = models.ImageField(upload_to=get_image_path, blank=True)
	cover_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(50, 50)], source='cover', format='JPEG', options={'quality': 90})
	cover_large = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(333, 500)], source='cover', format='JPEG', options={'quality': 90})
	cover_md = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(100, 170)], source='cover', format='JPEG', options={'quality': 90})

	def __str__(self):
		return "%s - %s" % (self.book.title, self.get_format_display())

class Review(models.Model):
	reader = models.ForeignKey(get_user_model(), related_name="+", on_delete=models.CASCADE)
	started = models.DateTimeField()
	finished = models.DateTimeField()
	edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
	critique = models.TextField(blank=True)
	one_sentence = models.CharField(max_length=300, null=True, default=None, blank=True)
	recommend = models.BooleanField()

	def __str__(self):
		return self.one_sentence

#I should consider doing this as a tagging module of some sort. The advantage of having it being "keywords" like this
#is we can also attribute the tag/keyword to the user.
class Keyword(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	reader = models.ForeignKey(get_user_model(), related_name='+', on_delete=models.CASCADE)
	keyword = models.CharField(max_length=100)

class QuoteType(models.Model):
	name = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Quote(models.Model):
	edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
	reader = models.ForeignKey(get_user_model(), related_name='+', on_delete=models.CASCADE)
	quote_type = models.ForeignKey(QuoteType, on_delete=models.CASCADE)
	quote = models.TextField()
	page = models.IntegerField()

	def __str__(self):
		return self.quote

class Note(models.Model):
	quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
	reader = models.ForeignKey(get_user_model(), related_name='+', on_delete=models.CASCADE)
	note = models.TextField()

	def __str__(self):
		return self.note

class Radar(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	maturity = models.IntegerField()
	violence = models.IntegerField()
	action = models.IntegerField()
	epic = models.IntegerField()
	world = models.IntegerField()
	realism = models.IntegerField()
	modernity = models.IntegerField()
	humor = models.IntegerField()

class Shelf(models.Model):
	reader = models.ForeignKey(get_user_model(), related_name='+', on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	private = models.BooleanField()

	def __str__(self):
		return self.name

class ShelfDetail(models.Model):
	shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

#will probably be able to do this just by pulling in the current status from goodreads
class Currently(models.Model):
	edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
	reader = models.ForeignKey(get_user_model(), related_name='+', on_delete=models.CASCADE)
	page = models.IntegerField()

class Favorite(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	user = models.ForeignKey(get_user_model(), related_name='+', on_delete=models.CASCADE)
	rank = models.IntegerField()
	comment = models.TextField()

# ************************************************************** #
# ************************ list data *************************** #
# ************************************************************** #

class List(models.Model):
	list_name = models.CharField(max_length=200)
	list_descr = models.CharField(max_length=200)
	user = models.ForeignKey(get_user_model(), related_name="+", on_delete=models.CASCADE) #this is the person who created it, and it will always be here
	def __str__(self):
		return self.list_name
		return "%s - %s" % (self.list_name, self.list_descr)
	def get_absolute_url(self):
		return "/list/%i/" % self.id
	def get_edit_url(self):
		return "/edit/list/%i/" % self.id
	def get_delete_url(self):
		return "/delete/list/%i/" % self.id	
	def get_add_url(self):
		return "/add/list/"

class ListDetail(models.Model):
	list = models.ForeignKey(List, related_name="list_details", on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

# ************************************************************** #
# *********************** series data ************************** #
# ************************************************************** #

class Series(models.Model):
	name = models.CharField(max_length=200)
	count = models.IntegerField()

	def __str__(self):
		return self.name

class SeriesDetail(models.Model):
	series = models.ForeignKey(Series, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	sequence = models.IntegerField()

	def __str__(self):
		return "%s - %s, %s of %s" % (self.series, self.book, self.sequence, self.series.count)

register(Book)