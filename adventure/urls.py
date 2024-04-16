from django.conf.urls import *
from django.urls import include, re_path
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.db.models import Count
from django.conf.urls.static import static
from adventure.models import *
from adventure import views as adventure_views

urlpatterns = [
	re_path(r'^$', adventure_views.GameList.as_view(), name='game-list'),
	re_path(r'^about/$', TemplateView.as_view(template_name = 'adventure/base_about.html'), name='about-page'),
	re_path(r'^autocomplete/$',adventure_views.autocomplete, name='adv-autocomplete'),
	re_path(r'^noresults/', TemplateView.as_view(template_name = 'adventure/base_noresults.html'), name='no-results'),
	re_path(r'^game/(?P<pk>\d+)/(?P<character>\d+)/(?P<level>\d+)/', adventure_views.GameView.as_view(), name='game-view'),
	re_path(r'^story/(?P<word>[\w ]+)/(?P<game>\d+)/(?P<character>\d+)/(?P<level>\d+)/', adventure_views.story_line, name='story-view'),
	re_path(r'^level/option/(?P<game>\d+)/(?P<level>\d+)/', adventure_views.level_options, name='level-options'),
	re_path(r'^word/(?P<game>\d+)/', login_required(adventure_views.WordList.as_view()), name='word-list'),
	re_path(r'^word/copy/(?P<current_game>\d+)/', adventure_views.copy_word_list, name='copy-word-list'),
]