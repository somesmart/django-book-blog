from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.views.generic.simple import direct_to_template
from django.db.models import Count
from sssd.adventure.models import *
from sssd.adventure.views import *

urlpatterns = patterns('',
	url(r'^$', GameList.as_view(), name='game-list'),
	url(r'^about/$', direct_to_template, { 'template': 'adventure/base_about.html'}, name='about-page'),
	url(r'^autocomplete/$','sssd.adventure.views.autocomplete', name='adv-autocomplete'),
	url(r'^noresults/', direct_to_template, { 'template': 'adventure/base_noresults.html' }, name='no-results'),
	url(r'^game/(?P<pk>\d+)/(?P<character>\d+)/(?P<level>\d+)/', GameView.as_view(), name='game-view'),
	url(r'^story/(?P<word>[\s\w+])/(?P<game>\d+)/(?P<character>\d+)/(?P<level>\d+)/', 'sssd.adventure.views.story_line', name='story-view'),
	url(r'^level/option/(?P<game>\d+)/(?P<level>\d+)/', 'sssd.adventure.views.level_options', name='level-options'),
	url(r'^word/(?P<game>\d+)/', login_required(WordList.as_view()), name='word-list'),
	url(r'^word/copy/(?P<current_game>\d+)/', 'sssd.adventure.views.copy_word_list', name='copy-word-list'),
)