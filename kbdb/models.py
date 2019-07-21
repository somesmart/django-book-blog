from django.db import models
from django.template.defaultfilters import slugify
from markdownx.models import MarkdownxField
import os

class RoundType(models.Model):
	""" The type of round that you are building """
	name = models.TextField(max_length=100)
	slug = models.SlugField()

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(RoundType, self).save(*args, **kwargs)

class Round(models.Model):
	""" The name of the round and a full description if necessary """
	round_type = models.ForeignKey(RoundType, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	description = MarkdownxField(blank=True)

	def __str__(self):
		return self.name

class LessonType(models.Model):
	""" The type of lesson that you are conducting """
	name = models.TextField(max_length=100)
	slug = models.SlugField()

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(LessonType, self).save(*args, **kwargs)

class Lesson(models.Model):
	""" The lesson you are conducting """
	date = models.DateField()
	lesson_type = models.ForeignKey(LessonType, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.date)

class LessonRound(models.Model):
	""" The rounds that make up the lesson you are conducting """
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
	round_number = models.IntegerField()
	round = models.ForeignKey(Round, on_delete=models.CASCADE)