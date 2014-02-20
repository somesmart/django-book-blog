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
from sssd.adventure.models import *
# from sssd.adventure.forms import *
from decimal import *
from datetime import datetime
import urllib2
from xml.dom.minidom import parseString

# ****************************************************************** #
# ********************* autocomplete views ************************* #
# ****************************************************************** #

def autocomplete(request):
	if request.method == "GET":
		if request.GET.has_key(u'term'):
			value = request.GET[u'term']
			search = request.GET[u'search']
			results = []
			if search == "word":
				# Ignore queries shorter than length 3
				if len(value) > 2:
					model_results = Word.objects.filter(word_descr__icontains=value)
					for word in model_results:
						data = {'id': word.id, 'label': word.word_descr }
						results.append(data)
					json = simplejson.dumps(results)
					return HttpResponse(json, mimetype='application/json')
				else:
					return HttpResponseRedirect('/noresults/')
		else:
			return HttpResponseRedirect('/noresults/')

def story_line(request, word, game, character, level):
	wordgroup = WordGroup.objects.select_related().get(word__word_descr=word)
	results = []
	line = Story.objects.select_related().get(game__id=game, character__id=character, level__id=level, wordgroup__id=wordgroup.id)
	data = {'id': line.id, 'character_id': line.character.id, 'next_level': line.next_level.id, 'text': line.text }
	results.append(data)
	json = simplejson.dumps(results)
	return HttpResponse(json, mimetype='application/json')

def level_options(request, game, level):
    results = ''
    level_results = LevelCharacter.objects.select_related().filter(game__id=game, level__id=level)
    for option in level_results:
        html = "<option value='" + str(option.character.id) + "'>" + option.character.first_name  + ' ' + option.character.last_name + "</option>"
        results = results + html
    return HttpResponse(results)    

class GameView(DetailView):
	template_name='adventure/base_game.html'
	context_object_name = 'game_play'

	def get_queryset(self):
		return Story.objects.select_related().filter(game__id=self.kwargs['pk'], character__id=self.kwargs['character'], level__id=self.kwargs['level'])