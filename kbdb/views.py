from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.db.models import Q, Count, Sum, Min, Max
from django.views.generic import DetailView, ListView, UpdateView, CreateView, FormView
from django.urls import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from kbdb.models import *
from kbdb.forms import *
from decimal import *
from datetime import datetime
import urllib.request, urllib.error, urllib.parse
from xml.dom.minidom import parseString

# ****************************************************************** #
# ********************* autocomplete views ************************* #
# ****************************************************************** #

def autocomplete(request):
	if request.method == "GET":
		if 'term' in request.GET:
			value = request.GET['term']
			search = request.GET['search']
			results = []
			if search == "round":
				if len(value) > 0:
					rounds = Round.objects.filter(name__icontains=value)
					for rnd in rounds:
						data = {'id': rnd.id, 'label': rnd.name }
						results.append(data)
					json_results = json.dumps(results)
					return HttpResponse(json_results, content_type='application/json')
				else:
					return HttpResponseRedirect('/noresults/')
		else:
			return HttpResponseRedirect('/noresults/')

# ****************************************************************** #
# ************************** kbdb views **************************** #
# ****************************************************************** #

class RoundView(DetailView):
	template_name='kbdb/base_round.html'
	model = Round

class RoundListView(ListView):
	template_name='kbdb/base_round_list.html'
	queryset= Round.objects.select_related().order_by('name')
	context_object_name = 'round_list'
	paginate_by = 25

class LessonView(DetailView):
	template_name='kbdb/base_lesson.html'
	model = Lesson

class LessonListView(ListView):
	template_name='kbdb/base_lesson_list.html'
	queryset=Lesson.objects.select_related().order_by('-date')
	# queryset=Lesson.objects.select_related().order_by('-date').annotate(round_count=Count('lessonround__round'))
	context_object_name = 'lesson_list'
	paginate_by = 25

class LessonCreateView(CreateView):
	template_name = 'kbdb/base_lesson_create.html'
	model = Lesson
	form_class = LessonForm

	def form_valid (self, form):
		context = self.get_context_data()
		lessonround_form = context['lessonround_form']
		if listdetail_form.is_valid():
			return HttpResponseRedirect('/lesson/')
		else:
			return self.render_to_response(self.get_context_data(form=form))

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(LessonCreateView, self).get_context_data(**kwargs)
		if self.request.POST:
			context['lessonround_form'] = LessonRoundFormSet(self.request.POST, instance=self.object)
		else:
			context['lessonround_form'] = LessonRoundFormSet(instance=self.object)
		return context