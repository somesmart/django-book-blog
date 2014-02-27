from django.db import models
from django.template.defaultfilters import slugify
import os

class Game(models.Model):
	name = models.TextField(max_length=100)
	slug = models.SlugField()

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			# Newly created object, so set slug
			self.slug = slugify(self.name)

		super(Game, self).save(*args, **kwargs)

class Character(models.Model):
	game = models.ForeignKey(Game)
	last_name = models.CharField(max_length=200, null=True, default=None, blank=True)
	first_name = models.CharField(max_length=200, null=True, default=None, blank=True)
	notes = models.CharField(max_length=200, null=True, default=None, blank=True)

	def __unicode__(self):
		return u"%s %s" % (self.first_name, self.last_name)	

class Level(models.Model):
	game = models.ForeignKey(Game)
	level_descr = models.CharField(max_length=200)

	def __unicode__(self):
		return self.level_descr

class LevelCharacter(models.Model):
	game = models.ForeignKey(Game)
	level = models.ForeignKey(Level)
	character = models.ForeignKey(Character)

class WordGroup(models.Model):
	group_descr = models.CharField(max_length=100)

	def __unicode__(self):
		return self.group_descr

class Word(models.Model):
	wordgroup = models.ForeignKey(WordGroup)
	game = models.ForeignKey(Game)
	word_descr = models.CharField(max_length=100)

	def __unicode__(self):
		return self.word_descr

class Story(models.Model):
	game = models.ForeignKey(Game)
	level = models.ForeignKey(Level)
	character = models.ForeignKey(Character)
	wordgroup = models.ForeignKey(WordGroup)
	next_level = models.ForeignKey(Level, related_name="next_level")
	text = models.TextField()

	class Meta:
		verbose_name_plural = "stories"

	def __unicode__(self):
		return self.text

class Unknown(models.Model):
	game = models.ForeignKey(Game)
	level = models.ForeignKey(Level)
	character = models.ForeignKey(Character)
	term = models.CharField(max_length=100)
	attempts = models.IntegerField()

	def __unicode__(self):
		return self.term