from django.conf.urls import *
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from somesmart.models import *
from somesmart.views import *

admin.autodiscover()

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^adventure/', include('adventure.urls')),
	url(r'^cashflow/', include('cashflow.urls')),
	url(r'^lotr/', include('lotr.urls')),
	url(r'^nature/', include('nature.urls')),
	url(r'^', include('somesmart.urls')),
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)