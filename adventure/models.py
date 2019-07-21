from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
import os

class Game(models.Model):
	STATUS = (
		(1, 'Public'),
		(2, 'Draft'),
	)

	name = models.TextField(max_length=100)
	slug = models.SlugField()
	creator = models.ForeignKey(get_user_model(), related_name='+', on_delete=models.CASCADE)
	status = models.IntegerField(choices=STATUS)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			# Newly created object, so set slug
			self.slug = slugify(self.name)

		super(Game, self).save(*args, **kwargs)

class Character(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	last_name = models.CharField(max_length=200, null=True, default=None, blank=True)
	first_name = models.CharField(max_length=200, null=True, default=None, blank=True)
	notes = models.CharField(max_length=200, null=True, default=None, blank=True)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)	

class Level(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	level_descr = models.CharField(max_length=200)

	def __str__(self):
		return self.level_descr

class LevelCharacter(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	level = models.ForeignKey(Level, on_delete=models.CASCADE)
	character = models.ForeignKey(Character, on_delete=models.CASCADE)

class WordGroup(models.Model):
	group_descr = models.CharField(max_length=100)

	def __str__(self):
		return self.group_descr

class Word(models.Model):
	wordgroup = models.ForeignKey(WordGroup, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	word_descr = models.CharField(max_length=100)

	def __str__(self):
		return self.word_descr

class Story(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	level = models.ForeignKey(Level, on_delete=models.CASCADE)
	character = models.ForeignKey(Character, on_delete=models.CASCADE)
	wordgroup = models.ForeignKey(WordGroup, on_delete=models.CASCADE)
	next_level = models.ForeignKey(Level, related_name="next_level", on_delete=models.CASCADE)
	text = models.TextField()

	class Meta:
		verbose_name_plural = "stories"

	def __str__(self):
		return self.text

class Unknown(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	level = models.ForeignKey(Level, on_delete=models.CASCADE)
	character = models.ForeignKey(Character, on_delete=models.CASCADE)
	term = models.CharField(max_length=100)
	attempts = models.IntegerField()

	def __str__(self):
		return self.term

class Generic(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	wordgroup = models.ForeignKey(WordGroup, on_delete=models.CASCADE)
	text = models.TextField()

	def __str__(self):
		return self.text