from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import os

class Location(models.Model):
	name = models.CharField(max_length=100)
	x_position = models.DecimalField(max_digits=15, decimal_places=9, default=0)
	y_postion = models.DecimalField(max_digits=15, decimal_places=9, default=0)

	def __str__(self):
		return self.name

class Journey(models.Model):
	short_description = models.CharField(max_length=250)
	long_description = models.TextField()
	start_location = models.ForeignKey(Location, related_name='journey_start', on_delete=models.CASCADE)
	end_location = models.ForeignKey(Location, related_name='journey_end', on_delete=models.CASCADE)

	def __str__(self):
		return self.short_description

class Character(models.Model):
	first_name = models.CharField(max_length=100, blank=True)
	last_name = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

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

	EVENT_MONTH = (
		(1, 'January'),
		(2, 'February'),
		(3, 'March'),
		(4, 'April'),
		(5, 'May'),
		(6, 'June'),
		(7, 'July'),
		(8, 'August'),
		(9, 'September'),
		(10, 'October'),
		(11, 'November'),
		(12, 'December'),
	)

	event_month = models.IntegerField(choices=EVENT_MONTH)
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
	journey = models.ForeignKey(Journey, on_delete=models.CASCADE)

	def __str__(self):
		return self.deck

class CharacterEvent(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	character =	models.ForeignKey(Character, on_delete=models.CASCADE)