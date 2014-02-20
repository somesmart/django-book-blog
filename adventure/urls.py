from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.views.generic.simple import direct_to_template
from django.db.models import Count
from sssd.adventure.models import *
from sssd.adventure.views import *

urlpatterns = patterns('',
	#home page
	url(r'^$',ListView.as_view(queryset=Game.objects.order_by('name'),context_object_name='game_list',template_name='adventure/base_index.html')),
	url(r'^about/$', direct_to_template, { 'template': 'adventure/base_about.html'}, name='about-page'),
	url(r'^autocomplete/$','sssd.adventure.views.autocomplete', name='autocomplete'),
	url(r'^noresults/', direct_to_template, { 'template': 'adventure/base_noresults.html' }, name='no-results'),
	url(r'^game/(?P<pk>\d+)/(?P<character>\d+)/(?P<level>\d+)/', GameView.as_view(), name='game-view'),
	#the next story line
	url(r'^story/(?P<word>\w+)/(?P<game>\d+)/(?P<character>\d+)/(?P<level>\d+)/', 'sssd.adventure.views.story_line', name='story-view'),
	url(r'^level/option/(?P<game>\d+)/(?P<level>\d+)/', 'sssd.adventure.views.level_options', name='level-options'),
	#url(r'^unknown/<P<word>[\w\s]+)/(?P<game>\d+)/(?P<character>\d+)/(?P<level>\d+)', UnknownCreate.as_view(), name='unknown-create'),
)