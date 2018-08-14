from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.db.models import Count
from django.conf import settings
from django.conf.urls.static import static
from ornaments.models import *
from ornaments import views as ornament_views

urlpatterns = [
	url(r'^$', ornament_views.OrnamentList.as_view(), name='ornament-list'),
	url(r'^ornament/(?P<pk>\d+)/', ornament_views.OrnamentView.as_view(), name='ornament-view'),
	url(r'^giver/(?P<pk>\d+)/', ornament_views.GiverView.as_view(), name='giver-view'),
	url(r'^receiver/(?P<pk>\d+)/', ornament_views.ReceiverView.as_view(), name='receiver-view'),
	url(r'^year/(?P<year>\d+)/$', ornament_views.YearView.as_view(), name='ornament-year')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)