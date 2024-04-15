from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.db.models import Count
from django.conf.urls.static import static
from kbdb.models import *
from kbdb import views as kbdb_views

urlpatterns = [
	re_path(r'^$', kbdb_views.LessonListView.as_view(), name='lesson-list'),
	re_path(r'^autocomplete/$',kbdb_views.autocomplete, name='kbdb-autocomplete'),
	re_path(r'^noresults/', TemplateView.as_view(template_name = 'somesmart/base_noresults.html'), name='no-results'),
	re_path(r'^round/(?P<pk>\d+)/', kbdb_views.RoundView.as_view(), name='round-view'),
	re_path(r'^round/$', kbdb_views.RoundListView.as_view(), name='round-list'),
	re_path(r'^lesson/(?P<pk>\d+)/', kbdb_views.LessonView.as_view(), name='lesson-view'),
	re_path(r'^lesson/add/', kbdb_views.LessonCreateView.as_view(), name='lesson-add'),
	re_path(r'^lesson/$', kbdb_views.LessonListView.as_view(), name='lesson-list'),
]