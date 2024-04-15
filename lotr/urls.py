from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.db.models import Count
from lotr.models import *
from lotr.views import *

urlpatterns = [
	re_path(r'^$', TodayEvent.as_view(), name='lotr-home'),
	re_path(r'^noresults/', TemplateView.as_view(template_name = 'lotr/base_noresults.html'), name='no-results'),
	re_path(r'^event/(?P<pk>\d+)/$', EventView.as_view(), name='event-view'),
	re_path(r'^event/month/(?P<month>\d+)/', EventByMonth.as_view(), name='event-month-view'),
	re_path(r'^event/date/(?P<month>\d+)/(?P<day>\d+)/$', EventByDate.as_view(), name='event-date-view'),
	re_path(r'^journey/(?P<pk>\d+)/$', JourneyView.as_view(), name='journey-view'),
]