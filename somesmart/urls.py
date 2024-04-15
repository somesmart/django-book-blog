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
	re_path('admin/', admin.site.urls),
	re_path(r'^adventure/', include('adventure.urls')),
	# re_path(r'^cashflow/', include('cashflow.urls')),
	re_path(r'^lotr/', include('lotr.urls')),
	re_path(r'^nature/', include('nature.urls')),
	re_path(r'^ornaments/', include('ornaments.urls')),
	# re_path(r'^kbdb/', include('kbdb.urls')),
	#re_path(r'^markdownx/', include('markdownx.urls')),
	#re_path(r'^wger/', include('wger.urls')),
	#home page
	re_path(r'^$',
		ListView.as_view(
			queryset=Review.objects.select_related().annotate(reviewed=Count('id')).order_by('-finished')[:10],
			context_object_name='recent_reads',
			template_name='somesmart/base_index.html')),
	#about page
	re_path(r'^about/$', TemplateView.as_view(template_name = 'somesmart/base_about.html'), name='about-page'),
	#book details
	re_path(r'^book/(?P<pk>\d+)/', somesmart_views.BookView.as_view(), name='book-view'),
	re_path(r'^author/(?P<pk>\d+)/', somesmart_views.AuthorView.as_view(), name='author-view'),
	re_path(r'^my-books/$', TemplateView.as_view(template_name = 'somesmart/base_mybooks.html'), name='my-books'),
	#charts
	re_path(r'^charts/$', somesmart_views.GlobalStats.as_view(), name='charts'),
	re_path(r'^charts/(?P<chart>[-\w]+)/(?P<option>[\w\d ]+)$', somesmart_views.ChartGenerate.as_view(), name='chart-generate'),
	re_path(r'^stats/global/$', somesmart_views.get_global_stats, name='global-stats'),
	#quote pages
	re_path(r'^quote/list/$', somesmart_views.QuoteList.as_view(), name='quote-list'),
	re_path(r'^quote/type/(?P<type>\d+)/$',somesmart_views.QuoteTypeList.as_view(), name='quote-type-list'),
	re_path(r'^quote/author/(?P<author>\d+)/',somesmart_views.QuoteAuthorList.as_view(), name='quote-author-list'),
	re_path(r'^quote/book/(?P<book>\d+)/',somesmart_views.QuoteBookList.as_view(), name='quote-book-list'),
	re_path(r'^quote/(?P<pk>\d+)/', somesmart_views.QuoteView.as_view(), name='quote-view'),
	re_path(r'^quote/random/$', somesmart_views.get_random_quote, name='random-quote'),
	#read details
	re_path(r'^review/(?P<pk>\d+)/', somesmart_views.ReviewView.as_view(), name='review-view'),
	re_path(r'^review/book/(?P<pk>\d+)/', somesmart_views.ReviewByBook.as_view(), name='review-by-book'),
	re_path(r'^review/list/$', somesmart_views.ReviewList.as_view(), name='review-list'),
	re_path(r'^review/list/(?P<genre>[-\w]+)/$', somesmart_views.ReviewGenreList.as_view(), name='review-genre-list'),
	#shelf details
	re_path(r'^shelf/(?P<pk>\d+)/', somesmart_views.ShelfView.as_view(), name='shelf-view'),
	#automplete all pass to the same view
	re_path(r'autocomplete/$',somesmart_views.autocomplete, name='autocomplete'),
	re_path(r'gr/current/$', somesmart_views.get_gr_current, name='get-gr-current'),
	#lists
	re_path(r'^list/(?P<pk>\d+)/', somesmart_views.ListDetailView.as_view(), name='list-view'),
	re_path(r'^list/$', somesmart_views.ListSummary.as_view(), name='list-summary'),
	re_path(r'^add/list/$', login_required(somesmart_views.ListCreateView.as_view(template_name='somesmart/base_list_create.html')), name='list-add'),
	re_path(r'^add/list/(?P<list>\d+)/item/(?P<book>\d+)/$', somesmart_views.add_list_item),
	re_path(r'^copy/list/(?P<list>\d+)/$', somesmart_views.copy_list, name='list-copy'),
	re_path(r'^edit/list/(?P<pk>\d+)/$', login_required(somesmart_views.ListUpdate.as_view(template_name='somesmart/base_list_update.html'))),
	re_path(r'^delete/list/item/(?P<pk>\d+)/$', somesmart_views.delete_list_item),
	re_path(r'^delete/list/(?P<pk>\d+)/$', somesmart_views.delete_list),
	#favorites
	re_path(r'^favorites/$', somesmart_views.FavoriteList.as_view(), name='favorite-list'),
	re_path(r'^favorites/(?P<genre>[-\w]+)/$', somesmart_views.FavoriteGenreList.as_view(), name='favorite-genre-list'),
	#tags
	re_path(r'^tags/current/$', somesmart_views.current_tags, name='current-tags'),
	re_path(r'^tags/book/(?P<book>\d+)/$', somesmart_views.book_tags, name='book-tags'),
	re_path(r'^tags/book/(?P<book>\d+)/save/$', somesmart_views.save_tags, name='save-tags'),
	re_path(r'^tags/book/(?P<book>\d+)/related/$', somesmart_views.get_related, name='related-books'),
	re_path(r'^tags/search/(?P<tag>[\w ]+)/$',somesmart_views.TagListView.as_view(), name='search-tags'),
	re_path(r'^tags/cloud/(?P<min_count>\d+)/$', somesmart_views.get_cloud, name='tag-cloud'),
	#the blog
	# re_path(r'^weblog/', include('zinnia.urls', namespace='zinnia')),
	re_path(r'^comments/', include('django_comments.urls')),
	re_path(r'^contact/', include('contact_form.urls')),
	re_path(r'noresults/', TemplateView.as_view(template_name = 'somesmart/base_noresults.html'), name='no-results'),
	#legacy urls
	re_path(r'^books/bookinfo\.php$', somesmart_views.bookinfo_php, name='bookinfo-php'),
	re_path(r'^bookinfo\.php$', somesmart_views.bookinfo_php, name='bookinfo-php'),
	re_path(r'^reviews/$', somesmart_views.bookinfo_php, name='review-old'),
	#malformatted archive links go to the homepage
	re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/', ListView.as_view(
			queryset=Review.objects.select_related().annotate(reviewed=Count('id')).order_by('-finished')[:10],
			context_object_name='recent_reads',
			template_name='somesmart/base_index.html')),
	# re_path(r'^(?P<year>\d+)/(?P<slug>[-\w]+)/', somesmart_views.zinnia_entry_detail, name='custom-zinnia'),
	# re_path(r'^feeds/$', somesmart_views.zinnia_latest_feeds, name='custom-zinnia-latest'),
	re_path(r'^accounts/login/$', auth_views.LoginView, {'template_name': 'somesmart/base_login.html'}, name='account-login'),
	re_path(r'^accounts/logout/$', auth_views.LogoutView, {'template_name': 'somesmart/base_logged_out.html'}, name='account-logout'),
	#re_path(r'^todo/', include('todo.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
