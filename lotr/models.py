from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import os

class Location(models.Model):
	name = models.CharField(max_length=100)
	x_position = models.DecimalField(max_digits=15, decimal_places=9, default=0)
	y_postion = models.DecimalField(max_digits=15, decimal_places=9, default=0)

	def __unicode__(self):
		return self.name

class Journey(models.Model):
	short_description = models.CharField(max_length=250)
	long_description = models.TextField()
	start_location = models.ForeignKey(Location, related_name='journey_start')
	end_location = models.ForeignKey(Location, related_name='journey_end')

	def __unicode__(self):
		return self.short_description

class Character(models.Model):
	first_name = models.CharField(max_length=100, blank=True)
	last_name = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return u"%s %s" % (self.first_name, self.last_name)

class Event(models.Model):

	DAY_OF_WEEK = (
		(1, 'Sunday'),
		(2, 'Monday'),
		(3, 'Tuesday'),
		(4, 'Wednesday'),
		(5, 'Thursday'),
		(6, 'Friday'),
		(7, 'Saturday'),
	)

	event_month = models.IntegerField()
	event_day = models.IntegerField()
	shire_year = models.IntegerField()
	third_age_year = models.IntegerField()
	explicit = models.BooleanField()
	deck = models.CharField(max_length=250)
	description = models.TextField()
	week_day = models.IntegerField(choices=DAY_OF_WEEK)
	group_size = models.IntegerField()
	x_position = models.DecimalField(max_digits=15, decimal_places=9, default=0)
	y_postion = models.DecimalField(max_digits=15, decimal_places=9, default=0)
	journey = models.ForeignKey(Journey)

	def __unicode__(self):
		return self.deck

class CharacterEvent(models.Model):
	event = models.ForeignKey(Event)
	character =	models.ForeignKey(Character)