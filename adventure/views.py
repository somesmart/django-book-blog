from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.db.models import Q, Count, Sum
from django.views.generic import DetailView, ListView, UpdateView, CreateView, FormView
from django.urls import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from adventure.models import *
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
			game = request.GET['game']
			character = request.GET['character']
			level = request.GET['level']
			results = []
			if search == "word":
				if len(value) > 0:
					groups = WordGroup.objects.select_related().values('id').filter(word__word_descr__icontains=value).distinct()
					model_results = Story.objects.select_related().filter(wordgroup__id__in=groups, game__id=game, level__id=level, character__id=character)
					for word in model_results:
						data = {'id': word.wordgroup.id, 'label': word.wordgroup.group_descr }
						results.append(data)
					json_results = json.dumps(results)
					return HttpResponse(json_results, content_type='application/json')
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
		word = Word.objects.select_related().get(word_descr=word, game=game)
		word_group = WordGroup.objects.get(id=word.wordgroup.id)
		try:
			line = Story.objects.select_related().get(game=game, character=character, level=level, wordgroup__id=word_group.id)
			data = {'id': line.id, 'character_id': line.character.id, 'next_level': line.next_level.id, 'text': line.text }
			results.append(data)
			json_results = json.dumps(results)
			return HttpResponse(json_results, content_type='application/json')
		except Story.DoesNotExist:
			try:
				line = Generic.objects.select_related().get(game=game, wordgroup__id=word_group.id)
				data = data = {'id': line.id, 'character_id': character.id, 'next_level': level.id, 'text': line.text }
				results.append(data)
			except Generic.DoesNotExist:
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
			json_results = json.dumps(results)
			return HttpResponse(json_results, content_type='application/json')
	except Word.DoesNotExist:
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
		json_results = json.dumps(results)
		return HttpResponse(json_results, content_type='application/json')

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
			if 'story_id' in self.request.GET:
				stories = Story.objects.select_related().filter(id=self.request.GET['story_id'])
			else:
				stories = Story.objects.select_related().filter(game__id=self.kwargs['pk'], level__id=self.kwargs['level'])
		else: 
			stories = Story.objects.select_related().filter(game__id=self.kwargs['pk'], level__id=self.kwargs['level'])
		for story in stories:
			if first:
				return Story.objects.select_related().get(id=story.id)

	def get_context_data(self, **kwargs):
		context = super(GameView, self).get_context_data(**kwargs)
		if self.request.method == "GET":
			if 'story_id' in self.request.GET:
				context ['next_level'] = self.kwargs['level']
		return context

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

def copy_word_list(request, current_game):
	current_game = Game.objects.get(id=current_game)
	if request.method == "GET":
		if 'new_game' in request.GET:
			new_game = Game.objects.get(id=request.GET['new_game'])
	if request.user.id == new_game.creator.id:
		word_list = Word.objects.filter(game=current_game)
		if word_list:
			for item in word_list:
				new_game_list = Word(wordgroup=item.wordgroup, game=new_game, word_descr=item.word_descr)
				new_game_list.save()
		return HttpResponseRedirect('/adventure/')
	else:
		return HttpResponseRedirect('/noresults/')

class GameCreate(CreateView):
	template_name = 'adventure/base_game_create.html'
	model = Game
	#form_class = GameForm

	def form_valid (self, form):
		if form.is_valid():
			obj = form.save(commit=False)
			obj.creator = self.request.user
			obj.save()
		context = self.get_context_data()
		story_form = context['story_form']
		if story_form.is_valid():
			self.object = form.save()
			story_form.instance = self.object
			story_form.save()
			return HttpResponseRedirect('/adventure/')
		else:
			return self.render(request, self.get_context_data(form=form))

	def form_invalid(self, form):
		return self.render(request, self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(GameCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			context['story_form'] = StoryFormSet(self.request.POST, instance=self.object)
		else:
			context['story_form'] = StoryFormSet(instance=self.object)
		return context

def delete_game(request, pk):
	game_creator = Game.objects.select_related().get(id=pk)
	if request.user.id == game_creator.user.id:
		Game.objects.filter(id=pk).delete()
		return HttpResponse("success")
	else:
		return HttpResponse("you shouldn't be here")

class GameUpdate(UpdateView):
	template_name = 'nature/base_game_update.html'
	model = Game
	#form_class = GameForm

	def form_valid (self, form):
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			return HttpResponseRedirect('/list/')

	def get_context_data(self, **kwargs):
		context = super(GameUpdate, self).get_context_data(**kwargs)
		self.game_id = self.kwargs['pk']
		context['detail_list'] = Story.objects.select_related().filter(game__id=self.game_id).order_by('game__name')  
		return context		

def delete_game_story(request, pk):
	story_item = Story.objects.select_related().get(id=pk)
	if request.user.id == story_item.game.creator.id:
		Story.objects.filter(id=pk).delete()
		return HttpResponse("success")
	else:
		return HttpResponse("you shouldn't be here")

def add_game_story(request, game, level, character, wordgroup, next_level, text):
	game = Game.objects.select_related().get(id=game)
	wordgroup = WordGroup.objects.get(id=wordgroup)
	if request.user.id == game.creator.id:
		new_item = Story(game=game, character=character, level=level, wordgroup=wordgroup, next_level=next_level, text=text)
		new_item.save()
		return HttpResponse(new_item.id)
	else:
		return HttpResponse("you shouldn't be here")		