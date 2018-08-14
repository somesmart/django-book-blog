from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.db.models import Q, Count, Sum
from django.views.generic import DetailView, ListView, UpdateView, CreateView, FormView
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from ornaments.models import *
from decimal import *
from datetime import datetime
import urllib2
from xml.dom.minidom import parseString

# ****************************************************************** #
# *********************** ornament views *************************** #
# ****************************************************************** #

class OrnamentView(DetailView):
	template_name='ornaments/base_ornament.html'
	queryset = Ornament.objects.select_related()

class OrnamentList(ListView):
	template_name='ornaments/base_index.html'
	context_object_name = 'ornament_list'

	def get_queryset(self):
		return Ornament.objects.select_related().filter(year=datetime.now().year)

	def get_context_data(self, **kwargs):
		context = super(OrnamentList, self).get_context_data(**kwargs)
		context ['giver_list'] = Giver.objects.all()
		context ['receiver_list'] = Receiver.objects.all()
		return context

class GiverView(DetailView):
	template_name='ornaments/base_giver.html'
	queryset = Giver.objects.select_related()

class ReceiverView(DetailView):
	template_name='ornaments/base_receiver.html'
	queryset = Receiver.objects.select_related()

class YearView(ListView):
	template_name='ornaments/base_year.html'
	context_object_name = 'ornament_list'

	def get_queryset(self):
		return Ornament.objects.select_related().filter(year=self.kwargs['year'])