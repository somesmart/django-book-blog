from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.db.models import Q, Count, Sum
from django.views.generic import DetailView, ListView, UpdateView, CreateView, FormView
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from sssd.lotr.models import *
from decimal import *
from datetime import datetime

class TodayEvent(ListView):
	template_name='lotr/base_index.html'
	context_object_name = 'event_list'

	def get_queryset(self):
		self.tdy = datetime.now().date()
		return Event.objects.select_related().filter(event_day=self.tdy.day, event_month=self.tdy.month)

class EventView(DetailView):
	queryset = Event.objects.select_related()
	template_name='lotr/base_event.html'
	context_object_name = 'event_detail'

class EventByDate(ListView):
	template_name = 'lotr/base_event_by_date.html'
	context_object_name = 'event_list'

	def get_queryset(self):
		return Event.objects.select_related().filter(event_day=self.kwargs['day'], event_month=self.kwargs['month']).order_by('shire_year')

class JourneyView(DetailView):
	queryset = Journey.objects.select_related()
	template_name='lotr/base_journey.html'
	context_object_name = 'journey'