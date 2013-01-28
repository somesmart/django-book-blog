from django.db import models
from django.core.urlresolvers import reverse
import datetime
from django.contrib.auth.models import User
import os
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

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

	def __unicode__(self):
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
	parent_author = models.ForeignKey('self', blank=True, default=None, null=True, help_text='The real name of a pen name')

	def __unicode__(self):
		return u"%s %s" % (self.first_name, self.last_name)	

class Book(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey(Author)
	original_publication = models.DateTimeField()
	synopsis = models.TextField(blank=True)
	reading_age = models.IntegerField()
	content_advisory = models.TextField(blank=True)
	genre = models.ForeignKey(Genre)

	def __unicode__(self):
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

	book = models.ForeignKey(Book)
	isbn = models.CharField(max_length=20)
	published = models.DateTimeField()
	pages = models.IntegerField()
	format = models.IntegerField(choices=FORMAT)
	cover = models.ImageField(upload_to=get_image_path, blank=True)
	cover_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(50, 50)], image_field='cover', format='JPEG', options={'quality': 90})
	cover_large = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(333, 500)], image_field='cover', format='JPEG', options={'quality': 90})

	def __unicode__(self):
		return u"%s - %s" % (self.book.title, self.get_format_display())

class Review(models.Model):
	reader = models.ForeignKey(User, related_name="+")
	started = models.DateTimeField()
	finished = models.DateTimeField()
	edition = models.ForeignKey(Edition)
	critique = models.TextField(blank=True)
	one_sentence = models.CharField(max_length=300, null=True, default=None, blank=True)
	recommend = models.BooleanField()

	def __unicode__(self):
		return self.one_sentence

#I should consider doing this as a tagging module of some sort. The advantage of having it being "keywords" like this
#is we can also attribute the tag/keyword to the user.
class Keyword(models.Model):
	book = models.ForeignKey(Book)
	reader = models.ForeignKey(User, related_name='+')
	keyword = models.CharField(max_length=100)

class QuoteType(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name

class Quote(models.Model):
	edition = models.ForeignKey(Edition)
	reader = models.ForeignKey(User, related_name='+')
	quote_type = models.ForeignKey(QuoteType)
	quote = models.TextField()
	page = models.IntegerField()

	def __unicode__(self):
		return self.quote

class Note(models.Model):
	quote = models.ForeignKey(Quote)
	reader = models.ForeignKey(User, related_name='+')
	note = models.TextField()

	def __unicode__(self):
		return self.note

class Radar(models.Model):
	book = models.ForeignKey(Book)
	maturity = models.IntegerField()
	violence = models.IntegerField()
	action = models.IntegerField()
	epic = models.IntegerField()
	world = models.IntegerField()
	realism = models.IntegerField()
	modernity = models.IntegerField()
	humor = models.IntegerField()
	# maturity = fields.IntegerRangeField(range(1,10))
	# violence = fields.IntegerRangeField(range(1,10))
	# action = fields.IntegerRangeField(range(1,10))
	# epic = fields.IntegerRangeField(range(1,10))
	# world = fields.IntegerRangeField(range(1,10))
	# realism = fields.IntegerRangeField(range(1,10))
	# modernity = fields.IntegerRangeField(range(1,10))
	# humor = fields.IntegerRangeField(range(1,10))

class Shelf(models.Model):
	reader = models.ForeignKey(User, related_name='+')
	name = models.CharField(max_length=100)
	private = models.BooleanField()

	def __unicode__(self):
		return self.name

class ShelfDetail(models.Model):
	shelf = models.ForeignKey(Shelf)
	book = models.ForeignKey(Book)

#will probably be able to do this just by pulling in the current status from goodreads
class Currently(models.Model):
	edition = models.ForeignKey(Edition)
	reader = models.ForeignKey(User, related_name='+')
	page = models.IntegerField()