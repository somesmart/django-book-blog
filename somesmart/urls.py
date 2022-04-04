from django.conf.urls import *
from django.views.generic import *
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.db.models import Count
from django.contrib.auth import views as auth_views
from somesmart.models import *
from somesmart import views as somesmart_views
from tagging.views import TaggedObjectList

admin.autodiscover()

urlpatterns = [
	url('admin/', admin.site.urls),
	url(r'^adventure/', include('adventure.urls')),
	# url(r'^cashflow/', include('cashflow.urls')),
	url(r'^lotr/', include('lotr.urls')),
	url(r'^nature/', include('nature.urls')),
	url(r'^ornaments/', include('ornaments.urls')),
	# url(r'^kbdb/', include('kbdb.urls')),
	#url(r'^markdownx/', include('markdownx.urls')),
	#url(r'^wger/', include('wger.urls')),
	#home page
	url(r'^$',
		ListView.as_view(
			queryset=Review.objects.select_related().annotate(reviewed=Count('id')).order_by('-finished')[:10],
			context_object_name='recent_reads',
			template_name='somesmart/base_index.html')),
	#about page
	url(r'^about/$', TemplateView.as_view(template_name = 'somesmart/base_about.html'), name='about-page'),
	#book details
	url(r'^book/(?P<pk>\d+)/', somesmart_views.BookView.as_view(), name='book-view'),
	url(r'^author/(?P<pk>\d+)/', somesmart_views.AuthorView.as_view(), name='author-view'),
	url(r'^my-books/$', TemplateView.as_view(template_name = 'somesmart/base_mybooks.html'), name='my-books'),
	#charts
	url(r'^charts/$', somesmart_views.GlobalStats.as_view(), name='charts'),
	url(r'^charts/(?P<chart>[-\w]+)/(?P<option>[\w\d ]+)$', somesmart_views.ChartGenerate.as_view(), name='chart-generate'),
	url(r'^stats/global/$', somesmart_views.get_global_stats, name='global-stats'),
	#quote pages
	url(r'^quote/list/$', somesmart_views.QuoteList.as_view(), name='quote-list'),
	url(r'^quote/type/(?P<type>\d+)/$',somesmart_views.QuoteTypeList.as_view(), name='quote-type-list'),
	url(r'^quote/author/(?P<author>\d+)/',somesmart_views.QuoteAuthorList.as_view(), name='quote-author-list'),
	url(r'^quote/book/(?P<book>\d+)/',somesmart_views.QuoteBookList.as_view(), name='quote-book-list'),
	url(r'^quote/(?P<pk>\d+)/', somesmart_views.QuoteView.as_view(), name='quote-view'),
	url(r'^quote/random/$', somesmart_views.get_random_quote, name='random-quote'),
	#read details
	url(r'^review/(?P<pk>\d+)/', somesmart_views.ReviewView.as_view(), name='review-view'),
	url(r'^review/book/(?P<pk>\d+)/', somesmart_views.ReviewByBook.as_view(), name='review-by-book'),
	url(r'^review/list/$', somesmart_views.ReviewList.as_view(), name='review-list'),
	url(r'^review/list/(?P<genre>[-\w]+)/$', somesmart_views.ReviewGenreList.as_view(), name='review-genre-list'),
	#shelf details
	url(r'^shelf/(?P<pk>\d+)/', somesmart_views.ShelfView.as_view(), name='shelf-view'),
	#automplete all pass to the same view
	url(r'autocomplete/$',somesmart_views.autocomplete, name='autocomplete'),
	url(r'gr/current/$', somesmart_views.get_gr_current, name='get-gr-current'),
	#lists
	url(r'^list/(?P<pk>\d+)/', somesmart_views.ListDetailView.as_view(), name='list-view'),
	url(r'^list/$', somesmart_views.ListSummary.as_view(), name='list-summary'),
	url(r'^add/list/$', login_required(somesmart_views.ListCreateView.as_view(template_name='somesmart/base_list_create.html')), name='list-add'),
	url(r'^add/list/(?P<list>\d+)/item/(?P<book>\d+)/$', somesmart_views.add_list_item),
	url(r'^copy/list/(?P<list>\d+)/$', somesmart_views.copy_list, name='list-copy'),
	url(r'^edit/list/(?P<pk>\d+)/$', login_required(somesmart_views.ListUpdate.as_view(template_name='somesmart/base_list_update.html'))),
	url(r'^delete/list/item/(?P<pk>\d+)/$', somesmart_views.delete_list_item),
	url(r'^delete/list/(?P<pk>\d+)/$', somesmart_views.delete_list),
	#favorites
	url(r'^favorites/$', somesmart_views.FavoriteList.as_view(), name='favorite-list'),
	url(r'^favorites/(?P<genre>[-\w]+)/$', somesmart_views.FavoriteGenreList.as_view(), name='favorite-genre-list'),
	#tags
	url(r'^tags/current/$', somesmart_views.current_tags, name='current-tags'),
	url(r'^tags/book/(?P<book>\d+)/$', somesmart_views.book_tags, name='book-tags'),
	url(r'^tags/book/(?P<book>\d+)/save/$', somesmart_views.save_tags, name='save-tags'),
	url(r'^tags/book/(?P<book>\d+)/related/$', somesmart_views.get_related, name='related-books'),
	url(r'^tags/search/(?P<tag>[\w ]+)/$',somesmart_views.TagListView.as_view(), name='search-tags'),
	url(r'^tags/cloud/(?P<min_count>\d+)/$', somesmart_views.get_cloud, name='tag-cloud'),
	#the blog
	# url(r'^weblog/', include('zinnia.urls', namespace='zinnia')),
	url(r'^comments/', include('django_comments.urls')),
	url(r'^contact/', include('contact_form.urls')),
	url(r'noresults/', TemplateView.as_view(template_name = 'somesmart/base_noresults.html'), name='no-results'),
	#legacy urls
	url(r'^books/bookinfo\.php$', somesmart_views.bookinfo_php, name='bookinfo-php'),
	url(r'^bookinfo\.php$', somesmart_views.bookinfo_php, name='bookinfo-php'),
	url(r'^reviews/$', somesmart_views.bookinfo_php, name='review-old'),
	#malformatted archive links go to the homepage
	url(r'^(?P<year>\d{4})/(?P<month>\d{2})/', ListView.as_view(
			queryset=Review.objects.select_related().annotate(reviewed=Count('id')).order_by('-finished')[:10],
			context_object_name='recent_reads',
			template_name='somesmart/base_index.html')),
	# url(r'^(?P<year>\d+)/(?P<slug>[-\w]+)/', somesmart_views.zinnia_entry_detail, name='custom-zinnia'),
	# url(r'^feeds/$', somesmart_views.zinnia_latest_feeds, name='custom-zinnia-latest'),
	url(r'^accounts/login/$', auth_views.LoginView, {'template_name': 'somesmart/base_login.html'}, name='account-login'),
	url(r'^accounts/logout/$', auth_views.LogoutView, {'template_name': 'somesmart/base_logged_out.html'}, name='account-logout'),
	#url(r'^todo/', include('todo.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)