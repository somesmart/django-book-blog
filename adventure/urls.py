from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.views.generic.simple import direct_to_template
from django.db.models import Count
from sssd.adventure.models import *
from sssd.adventure.views import *

urlpatterns = patterns('',
	#home page
	url(r'^$', direct_to_template, { 'template': 'adventure/base_index.html'}, name='home-page'),
	url(r'^about/$', direct_to_template, { 'template': 'adventure/base_about.html'}, name='about-page'),
	#the next story line
	url(r'^story/(?P<wordgrou>\w+)/(?P<game>\d+)/(?P<character>\d+)/(?P<level>\d+)', StoryView.as_view(), name='story-view'),
	url(r'^unknown/<P<wordgroup>[\w\s]+)/(?P<game>\d+)/(?P<character>\d+)/(?P<level>\d+)', UnknownCreate.as_view(), name='unknown-create'),
)