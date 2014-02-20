from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.views.generic.simple import direct_to_template
from django.db.models import Count
from sssd.somesmart.models import *
from sssd.somesmart.views import *

urlpatterns = patterns('',
	#home page
	url(r'^$',
		ListView.as_view(
			queryset=Review.objects.select_related().annotate(reviewed=Count('id')).order_by('-finished')[:10],
			context_object_name='recent_reads',
			template_name='somesmart/base_index.html')),
	#about page
	url(r'^about/$', direct_to_template, { 'template': 'somesmart/base_about.html'}, name='about-page'),
	#book details
	url(r'^book/(?P<pk>\d+)/', BookView.as_view(), name='book-view'),
	url(r'^author/(?P<pk>\d+)/', AuthorView.as_view(), name='author-view'),
	url(r'^my-books/$', direct_to_template, { 'template': 'somesmart/base_mybooks.html'}, name='my-books'),
	#charts
	url(r'^charts/$', GlobalStats.as_view(), name='charts'),
	url(r'^charts/(?P<chart>[-\w]+)/(?P<option>[\s\w\d]+)$', ChartGenerate.as_view(), name='chart-generate'),
	#quote pages
	url(r'^quote/list/$', QuoteList.as_view(), name='quote-list'),
	url(r'^quote/type/(?P<type>\d+)/$',QuoteTypeList.as_view(), name='quote-type-list'),
	url(r'^quote/author/(?P<author>\d+)/',QuoteAuthorList.as_view(), name='quote-author-list'),
	url(r'^quote/book/(?P<book>\d+)/',QuoteBookList.as_view(), name='quote-book-list'),
	url(r'^quote/(?P<pk>\d+)/', QuoteView.as_view(), name='quote-view'),
	url(r'^quote/random/$', 'sssd.somesmart.views.get_random_quote', name='random-quote'),
	#read details
	url(r'^review/(?P<pk>\d+)/', ReviewView.as_view(), name='review-view'),
	url(r'^review/book/(?P<pk>\d+)/', ReviewByBook.as_view(), name='review-by-book'),
	url(r'^review/list/$', ReviewList.as_view(), name='review-list'),
	url(r'^review/list/(?P<genre>[-\w]+)/$', ReviewGenreList.as_view(), name='review-genre-list'),
	#shelf details
	url(r'^shelf/(?P<pk>\d+)/', ShelfView.as_view(), name='shelf-view'),
	#automplete all pass to the same view
	url(r'autocomplete/$','sssd.somesmart.views.autocomplete', name='autocomplete'),
	url(r'gr/current/$', 'sssd.somesmart.views.get_gr_current', name='get-gr-current'),
	#lists
	url(r'^list/(?P<pk>\d+)/', login_required(ListDetailView.as_view()), name='list-view'),
	url(r'^list/$', login_required(ListSummary.as_view()), name='list-summary'),
	url(r'^add/list/$', login_required(ListCreateView.as_view(template_name='somesmart/base_list_create.html')), name='list-add'),
	url(r'^add/list/(?P<list>\d+)/item/(?P<book>\d+)/$', 'sssd.somesmart.views.add_list_item'),
	url(r'^copy/list/(?P<list>\d+)/$', 'sssd.somesmart.views.copy_list', name='list-copy'),
	url(r'^edit/list/(?P<pk>\d+)/$', login_required(ListUpdate.as_view(template_name='somesmart/base_course_update.html'))),
	url(r'^delete/list/item/(?P<pk>\d+)/$', 'sssd.somesmart.views.delete_list_item'),
	url(r'^delete/list/(?P<pk>\d+)/$', 'sssd.somesmart.views.delete_list'),
	#the blog
	url(r'^blog/', include('zinnia.urls')),
	url(r'^blog/tags/', include('zinnia.urls.tags')),
	url(r'^blog/feeds/', include('zinnia.urls.feeds')),
	url(r'^blog/authors/', include('zinnia.urls.authors')),
	url(r'^blog/categories/', include('zinnia.urls.categories')),
	url(r'^blog/discussions/', include('zinnia.urls.discussions')),
	url(r'^blog/', include('zinnia.urls.entries')),
	url(r'^blog/', include('zinnia.urls.archives')),
	url(r'^blog/', include('zinnia.urls.shortlink')),
	url(r'^blog/', include('zinnia.urls.quick_entry')),
	url(r'^comments/', include('django.contrib.comments.urls')),
	(r'^contact/', include('contact_form.urls')),
	url(r'noresults/', direct_to_template, { 'template': 'somesmart/base_noresults.html' }, name='no-results'),
	#legacy urls
	url(r'^books/bookinfo\.php$', 'sssd.somesmart.views.bookinfo_php', name='bookinfo-php'),
	url(r'^bookinfo\.php$', 'sssd.somesmart.views.bookinfo_php', name='bookinfo-php'),
	url(r'^reviews/$', 'sssd.somesmart.views.bookinfo_php', name='review-old'),
	#malformatted archive links go to the homepage
	url(r'^(?P<year>\d{4})/(?P<month>\d{2})/', ListView.as_view(
			queryset=Review.objects.select_related().annotate(reviewed=Count('id')).order_by('-finished')[:10],
			context_object_name='recent_reads',
			template_name='somesmart/base_index.html')),
	url(r'^(?P<year>\d+)/(?P<slug>[-\w]+)/', 'sssd.somesmart.views.zinnia_entry_detail', name='custom-zinnia'),
	url(r'^feeds/$', 'sssd.somesmart.views.zinnia_latest_feeds', name='custom-zinnia-latest')
)