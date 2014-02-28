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
			game = request.GET[u'game']
			character = request.GET[u'character']
			level = request.GET[u'level']
			results = []
			if search == "word":
				# Ignore queries shorter than length 3
				if len(value) > 2:
					model_results = Story.objects.select_related().filter(wordgroup__group_descr__icontains=value, game__id=game, level__id=level, character__id=character)
					for word in model_results:
						data = {'id': word.wordgroup.id, 'label': word.wordgroup.group_descr }
						results.append(data)
					json = simplejson.dumps(results)
					return HttpResponse(json, mimetype='application/json')
				else:
					return HttpResponseRedirect('/noresults/')
		else:
			return HttpResponseRedirect('/noresults/')

# ****************************************************************** #
# *********************** adventure views ************************** #
# ****************************************************************** #

def story_line(request, word, game, character, level):
	results = []
	game = Game.objects.get(id=game)
	character = Character.objects.get(id=character)
	level = Level.objects.get(id=level)
	not_expected = "<p>Nothing happens.</p>"
	try:
		word_group = WordGroup.objects.select_related().get(word__word_descr=word)
		try:
			line = Story.objects.select_related().get(game=game, character=character, level=level, wordgroup__id=word_group.id)
			data = {'id': line.id, 'character_id': line.character.id, 'next_level': line.next_level.id, 'text': line.text }
			results.append(data)
			json = simplejson.dumps(results)
			return HttpResponse(json, mimetype='application/json')
		except Story.DoesNotExist:
			line = None
			try:
				unknown = Unknown.objects.get(game=game, level=level, character=character, term=word)
				unknown.attempts = unknown.attempts + 1
				unknown.save()
				data = {'id': 1, 'character_id': character.id, 'next_level': level.id, 'text': not_expected}
				results.append(data)
			except Unknown.DoesNotExist:
				Unknown(game=game, level=level, character=character, term=word, attempts=1).save()
				data = {'id': 1, 'character_id': character.id, 'next_level': level.id, 'text': not_expected}
				results.append(data)
			json = simplejson.dumps(results)
			return HttpResponse(json, mimetype='application/json')
	except WordGroup.DoesNotExist:
		word_group = None
		try:
			unknown = Unknown.objects.get(game=game, level=level, character=character, term=word)
			unknown.attempts = unknown.attempts + 1
			unknown.save()
			data = {'id': 1, 'character_id': character.id, 'next_level': level.id, 'text': not_expected}
			results.append(data)
		except Unknown.DoesNotExist:
			unknown = None
			Unknown(game=game, level=level, character=character, term=word, attempts=1).save()
			data = {'id': 1, 'character_id': character.id, 'next_level': level.id, 'text': not_expected}
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

class GameView(ListView):
	template_name='adventure/base_game.html'
	context_object_name = 'game_play'

	def get_queryset(self):
		first = True
		if self.request.method == "GET":
			if self.request.GET.has_key(u'story_id'):
				stories = Story.objects.select_related().filter(id=self.request.GET[u'story_id'])
			else:
				stories = Story.objects.select_related().filter(game__id=self.kwargs['pk'], level__id=self.kwargs['level'])
		for story in stories:
			if first:
				return Story.objects.select_related().get(id=story.id)

class GameList(ListView):
	template_name='adventure/base_index.html'
	context_object_name = 'game_list'

	def get_queryset(self):
		return Story.objects.select_related().filter(wordgroup__group_descr='start').order_by('game__name')

class WordList(ListView):
	template_name='adventure/base_word_list.html'
	context_object_name = 'word_list'

	def get_queryset(self):
		return Word.objects.select_related().filter(game__id=self.kwargs['game']).order_by('wordgroup', 'word_descr')

	def get_context_data(self, **kwargs):
		context = super(WordList, self).get_context_data(**kwargs)
		context ['current_game'] = self.kwargs['game']
		context ['game_list'] = Game.objects.exclude(id=self.kwargs['game']).filter(creator=self.request.user)
		return context