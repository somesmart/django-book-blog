from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q, Count, Sum
from django.views.generic import DetailView, ListView, UpdateView, CreateView, FormView
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from lotr.models import *
from decimal import *
from datetime import datetime

def get_dates(month, day):
	day = int(day)
	month = int(month)
	prev_day = day - 1
	next_day = day + 1
	prev_month = month
	next_month = month
	if day == 30:
		next_day = 1
		if month == 12:
			next_month = 1
		else:
			next_month = month + 1
	if day == 1:
		prev_day = 30
		if month == 1:
			prev_month = 12
		else:
			prev_month = month - 1
	dates = {'prev_month': prev_month, 'next_month': next_month, 'prev_day': prev_day, 'next_day': next_day}
	return dates

def get_month_dates(month):
	month = int(month)
	prev_month = month - 1
	next_month = month + 1
	if month == 1:
		prev_month = 12
	if month == 12:
		next_month = 1
	dates = {'prev_month': prev_month, 'next_month': next_month}
	return dates

class TodayEvent(ListView):
	template_name='lotr/base_index.html'
	context_object_name = 'event_list'

	def get_queryset(self):
		self.tdy = datetime.now().date()
		return Event.objects.select_related().filter(event_day=self.tdy.day, event_month=self.tdy.month)

	def get_context_data(self, **kwargs):
		context = super(TodayEvent, self).get_context_data(**kwargs)
		self.tdy = datetime.now().date()
		self.dates = get_dates(self.tdy.month, self.tdy.day)
		context ['dates'] = self.dates
		return context

class EventView(DetailView):
	queryset = Event.objects.select_related()
	template_name='lotr/base_event.html'
	context_object_name = 'event_detail'

	def get_context_data(self, **kwargs):
		context = super(EventView, self).get_context_data(**kwargs)
		self.event = Event.objects.get(pk=self.kwargs['pk'])
		self.dates = get_dates(self.event.event_month, self.event.event_day)
		context ['dates'] = self.dates
		return context

class EventByDate(ListView):
	template_name = 'lotr/base_event_by_date.html'
	context_object_name = 'event_list'

	def get_queryset(self):
		return Event.objects.select_related().filter(event_day=self.kwargs['day'], event_month=self.kwargs['month']).order_by('shire_year')

	def get_context_data(self, **kwargs):
		context = super(EventByDate, self).get_context_data(**kwargs)
		self.dates = get_dates(self.kwargs['month'], self.kwargs['day'])
		context ['dates'] = self.dates
		if self.kwargs['day'] == '31':
			context ['na'] = {'value': '<p>Unfortunately the 31st does not exist in the Shire calendar. Please try a different date.</p>'}
		return context

class EventByMonth(ListView):
	template_name = 'lotr/base_event_month.html'
	context_object_name = 'event_list'

	def get_queryset(self):
		return Event.objects.select_related().filter(event_month=self.kwargs['month']).order_by('event_day', 'shire_year')

	def get_context_data(self, **kwargs):
		context = super(EventByMonth, self).get_context_data(**kwargs)
		self.dates = get_month_dates(self.kwargs['month'])
		context ['dates'] = self.dates
		return context		

class JourneyView(DetailView):
	queryset = Journey.objects.select_related()
	template_name='lotr/base_journey.html'
	context_object_name = 'journey'