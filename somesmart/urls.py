from django.conf.urls import *
from django.views.generic import *
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from somesmart.models import *
from somesmart.views import *
from tagging.views import TaggedObjectList

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^adventure/', include('adventure.urls')),
	url(r'^cashflow/', include('cashflow.urls')),
	url(r'^lotr/', include('lotr.urls')),
	#home page
	url(r'^$',
		ListView.as_view(
			queryset=Review.objects.select_related().annotate(reviewed=Count('id')).order_by('-finished')[:10],
			context_object_name='recent_reads',
			template_name='somesmart/base_index.html')),
	#about page
	url(r'^about/$', TemplateView.as_view(template_name = 'somesmart/base_about.html'), name='about-page'),
	#book details
	url(r'^book/(?P<pk>\d+)/', BookView.as_view(), name='book-view'),
	url(r'^author/(?P<pk>\d+)/', AuthorView.as_view(), name='author-view'),
	url(r'^my-books/$', TemplateView.as_view(template_name = 'somesmart/base_mybooks.html'), name='my-books'),
	#charts
	url(r'^charts/$', GlobalStats.as_view(), name='charts'),
	url(r'^charts/(?P<chart>[-\w]+)/(?P<option>[\w\d ]+)$', ChartGenerate.as_view(), name='chart-generate'),
	url(r'^stats/global/$', 'somesmart.views.get_global_stats', name='global-stats'),
	#quote pages
	url(r'^quote/list/$', QuoteList.as_view(), name='quote-list'),
	url(r'^quote/type/(?P<type>\d+)/$',QuoteTypeList.as_view(), name='quote-type-list'),
	url(r'^quote/author/(?P<author>\d+)/',QuoteAuthorList.as_view(), name='quote-author-list'),
	url(r'^quote/book/(?P<book>\d+)/',QuoteBookList.as_view(), name='quote-book-list'),
	url(r'^quote/(?P<pk>\d+)/', QuoteView.as_view(), name='quote-view'),
	url(r'^quote/random/$', 'somesmart.views.get_random_quote', name='random-quote'),
	#read details
	url(r'^review/(?P<pk>\d+)/', ReviewView.as_view(), name='review-view'),
	url(r'^review/book/(?P<pk>\d+)/', ReviewByBook.as_view(), name='review-by-book'),
	url(r'^review/list/$', ReviewList.as_view(), name='review-list'),
	url(r'^review/list/(?P<genre>[-\w]+)/$', ReviewGenreList.as_view(), name='review-genre-list'),
	#shelf details
	url(r'^shelf/(?P<pk>\d+)/', ShelfView.as_view(), name='shelf-view'),
	#automplete all pass to the same view
	url(r'autocomplete/$','somesmart.views.autocomplete', name='autocomplete'),
	url(r'gr/current/$', 'somesmart.views.get_gr_current', name='get-gr-current'),
	#lists
	url(r'^list/(?P<pk>\d+)/', ListDetailView.as_view(), name='list-view'),
	url(r'^list/$', ListSummary.as_view(), name='list-summary'),
	url(r'^add/list/$', login_required(ListCreateView.as_view(template_name='somesmart/base_list_create.html')), name='list-add'),
	url(r'^add/list/(?P<list>\d+)/item/(?P<book>\d+)/$', 'somesmart.views.add_list_item'),
	url(r'^copy/list/(?P<list>\d+)/$', 'somesmart.views.copy_list', name='list-copy'),
	url(r'^edit/list/(?P<pk>\d+)/$', login_required(ListUpdate.as_view(template_name='somesmart/base_list_update.html'))),
	url(r'^delete/list/item/(?P<pk>\d+)/$', 'somesmart.views.delete_list_item'),
	url(r'^delete/list/(?P<pk>\d+)/$', 'somesmart.views.delete_list'),
	#favorites
	url(r'^favorites/$', FavoriteList.as_view(), name='favorite-list'),
	url(r'^favorites/(?P<genre>[-\w]+)/$', FavoriteGenreList.as_view(), name='favorite-genre-list'),
	#tags
	url(r'^tags/current/$', 'somesmart.views.current_tags', name='current-tags'),
	url(r'^tags/book/(?P<book>\d+)/$', 'somesmart.views.book_tags', name='book-tags'),
	url(r'^tags/book/(?P<book>\d+)/save/$', 'somesmart.views.save_tags', name='save-tags'),
	url(r'^tags/book/(?P<book>\d+)/related/$', 'somesmart.views.get_related', name='related-books'),
	url(r'^tags/search/(?P<tag>[\w ]+)/$',TagListView.as_view(), name='search-tags'),
	url(r'^tags/cloud/(?P<min_count>\d+)/$', 'somesmart.views.get_cloud', name='tag-cloud'),
	#the blog
	url(r'^weblog/', include('zinnia.urls', namespace='zinnia')),
	url(r'^comments/', include('django_comments.urls')),
	(r'^contact/', include('contact_form.urls')),
	url(r'noresults/', TemplateView.as_view(template_name = 'somesmart/base_noresults.html'), name='no-results'),
	#legacy urls
	url(r'^books/bookinfo\.php$', 'somesmart.views.bookinfo_php', name='bookinfo-php'),
	url(r'^bookinfo\.php$', 'somesmart.views.bookinfo_php', name='bookinfo-php'),
	url(r'^reviews/$', 'somesmart.views.bookinfo_php', name='review-old'),
	#malformatted archive links go to the homepage
	url(r'^(?P<year>\d{4})/(?P<month>\d{2})/', ListView.as_view(
			queryset=Review.objects.select_related().annotate(reviewed=Count('id')).order_by('-finished')[:10],
			context_object_name='recent_reads',
			template_name='somesmart/base_index.html')),
	url(r'^(?P<year>\d+)/(?P<slug>[-\w]+)/', 'somesmart.views.zinnia_entry_detail', name='custom-zinnia'),
	url(r'^feeds/$', 'somesmart.views.zinnia_latest_feeds', name='custom-zinnia-latest'),
	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'somesmart/base_login.html'}, name='account-login'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'somesmart/base_logged_out.html'}, name='account-logout'),
	# url(r'^todo/', include('todo.urls'))
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)