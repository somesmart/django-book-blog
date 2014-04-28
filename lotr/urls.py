from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.views.generic.simple import direct_to_template
from django.db.models import Count
from sssd.lotr.models import *
from sssd.lotr.views import *

urlpatterns = patterns('',
	url(r'^$', TodayEvent.as_view(), name='lotr-home'),
	url(r'^noresults/', direct_to_template, { 'template': 'lotr/base_noresults.html' }, name='no-results'),
	url(r'^event/(?P<pk>\d+)/$', EventView.as_view(), name='event-view'),
	url(r'^event/date/(?P<month>\d+)/(?P<day>\d+)/$', EventByDate.as_view(), name='event-date-view'),
	url(r'^journey/(?P<pk>\d+)/$', JourneyView.as_view(), name='journey-view'),
)