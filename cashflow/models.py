from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from recurrence.fields import RecurrenceField
from datetime import datetime, date
import os

class Budget(models.Model):
	STATUS = (
		(1, 'Public'),
		(2, 'Draft'),
	)

	name = models.TextField(max_length=100)
	slug = models.SlugField()
	creator = models.ForeignKey(User, related_name='+')
	status = models.IntegerField(choices=STATUS)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			# Newly created object, so set slug
			self.slug = slugify(self.name)

		super(Budget, self).save(*args, **kwargs)

class Category(models.Model):
	description = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = "categories"

	def __unicode__(self):
		return self.description

class Account(models.Model):
	name = models.CharField(max_length=100)
	balance = models.DecimalField(max_digits=15, decimal_places=2)
	balance_date = models.DateField()

	def __unicode__(self):
		return self.name

class BudgetAccount(models.Model):
	budget = models.ForeignKey(Budget)
	account = models.ForeignKey(Account)

class BudgetDetail(models.Model):
	budget = models.ForeignKey(Budget)
	category = models.ForeignKey(Category)
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	savings = models.BooleanField()

class Source(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class Transaction(models.Model):
	budget = models.ForeignKey(Budget)
	date = models.DateField()
	category = models.ForeignKey(Category)
	account = models.ForeignKey(Account)
	source = models.ForeignKey(Source)
	amount = models.DecimalField(max_digits=15, decimal_places=2)
	note = models.CharField(max_length=150, null=True, default=None, blank=True)
	reconciled = models.BooleanField()
	recurring = models.BooleanField()
	recurrences = RecurrenceField()

	def __unicode__(self):
		return self.note

	def save(self, *args, **kwargs):
		if self.recurring == True:
			self.recurrences.dtstart = datetime(self.date.year, self.date.month, self.date.day, 0, 0, 0)

		super(Transaction, self).save(*args, **kwargs)