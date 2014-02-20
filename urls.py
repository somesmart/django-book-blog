from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.contrib import admin
from sssd.somesmart.models import *
from sssd.somesmart.views import *

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^adventure/', include('sssd.adventure.urls')),
	url(r'^', include('sssd.somesmart.urls')),
)