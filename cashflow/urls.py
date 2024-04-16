from django.conf.urls import *
from django.urls import include, re_path
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.db.models import Count
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from cashflow.models import *
from cashflow.views import *

# If you already have a js_info_dict dictionary, just add
# 'recurrence' to the existing 'packages' tuple.
js_info_dict = {
	'packages': ('recurrence', ),
}

urlpatterns = [
	re_path(r'^$', RecentTransactions.as_view(), name='recent-transactions'),
	# re_path(r'^autocomplete/$','cashflow.views.autocomplete', name='cash-autocomplete'),
	re_path(r'^noresults/', TemplateView.as_view(template_name = 'cashflow/base_noresults.html'), name='no-results'),
	re_path(r'^forecast/(?P<budget>\d+)/$', ViewForecast.as_view(), name='view-forecast'),
	re_path(r'^trx/(?P<pk>\d+)$', ViewTrx.as_view(), name='view-trx'),
	re_path(r'^trx/add/(?P<pk>\d+)/$', AddTrx.as_view(), name='add-trx'),
	re_path(r'^trx/delete/(?P<pk>\d+)/$', 'cashflow.views.delete_trx', name='delete-trx'),
	re_path(r'^category/add/(?P<description>[\w ]+)/$', 'cashflow.views.add_category', name='add-category'),
	re_path(r'^source/add/(?P<name>[\w ]+)/$', 'cashflow.views.add_source', name='add-source'),
	re_path(r'success/', 'cashflow.views.success', name='post-success'),
	(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
] + staticfiles_urlpatterns()