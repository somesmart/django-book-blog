from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.db.models import Q, Count, Sum
from django.views.generic import DetailView, ListView, UpdateView, CreateView, FormView
from django.urls import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from somesmart.models import *
from zinnia.models import Entry
from somesmart.forms import *
from tagging.models import Tag, TaggedItem
from tagging.utils import LOGARITHMIC
from decimal import *
from datetime import datetime
import urllib.request, urllib.error, urllib.parse
from xml.dom.minidom import parseString

# ****************************************************************** #
# ********************* autocomplete views ************************* #
# ****************************************************************** #

def autocomplete(request):
	if request.method == "GET":
		if 'term' in request.GET:
			value = request.GET['term']
			search = request.GET['search']
			results = []
			if search == "title":
				# Ignore queries shorter than length 3
				if len(value) > 2:
					model_results = Book.objects.filter(title__icontains=value)
					for book in model_results:
						data = {'id': book.id, 'label': book.title }
						results.append(data)
					json_results = json.dumps(results)
					return HttpResponse(json_results, content_type='application/json')
				else:
					return HttpResponseRedirect('/noresults/')
			elif search == "primary_search":
				if len(value) > 3:
					model_results = Book.objects.select_related().filter(Q(title__icontains=value) | Q(author__last_name__icontains=value) | Q(author__first_name__icontains=value))
					data = None
					for book in model_results:
						try:
							data = {'id': '/book/' + str(book.id) + '/' + slugify(book.title) + '/', 'label': book.title }
						except:
							data = {'id': '/author/' + str(book.author.id) + '/', 'label': book.author.first_name + ' ' + book.author.last_name }
						results.append(data)
					json_results = json.dumps(results)
					return HttpResponse(json_results, content_type='application/json')
				else:
					return HttpResponseRedirect('/noresults/')
			elif search == "author":
				# Ignore queries shorter than length 4
				if len(value) > 3:
					model_results = Author.objects.filter(Q(last_name__icontains=value) | Q(first_name__icontains=value))
					for author in model_results:
						data = {'id': author.id, 'label': author.first_name + ' ' + author.last_name }
						results.append(data)
					json_results = json.dumps(results)
					return HttpResponse(json_results, content_type='application/json')
				else:
					return HttpResponseRedirect('/noresults/')
		else:
			return HttpResponseRedirect('/noresults/')

class BookView(DetailView):
	model = Book
	template_name='somesmart/base_book.html'

	# def get_context_data(self, **kwargs):
	# 	context = super(BookView, self).get_context_data(**kwargs)
	# 	try:
	# 		self.dtl = SeriesDetail.objects.values('series').filter(book__id=self.kwargs['pk']).distinct()
	# 		self.series = SeriesDetail.objects.select_related().filter(series=self.dtl).order_by('sequence')
	# 	except SeriesDetail.DoesNotExist:
	# 		self.series = None
	# 	context['series'] = self.series
	# 	return context

def bookinfo_php(request):
	if 'bookid' in request.GET:
		isbn = request.GET['bookid']
		book = Book.objects.select_related().get(edition__isbn=isbn)
		return redirect('book-view', pk=book.id)
	else:
		return HttpResponseRedirect('/review/list/')

def get_global_stats(request):
	book_total = Book.objects.aggregate(book_count=Count('id'))
	page_total = Edition.objects.aggregate(page_count=Sum('pages'))
	quote_total = Quote.objects.aggregate(quote_count=Count('id'))
	rec_total = Review.objects.filter(recommend=True).aggregate(rec_count=Count('id'))
	return render_to_response('somesmart/include_global_stats.html', {'global_stats' : book_total, 'page_total': page_total, 'quote_total': quote_total, 'rec_total': rec_total })

class GlobalStats(ListView):
	template_name='somesmart/base_charts.html'
	context_object_name = 'global_stats'

	def get_queryset(self):
		return Book.objects.aggregate(book_count=Count('id'))

	def get_context_data(self, **kwargs):
		context = super(GlobalStats, self).get_context_data(**kwargs)
		context ['page_total'] = Edition.objects.aggregate(page_count=Sum('pages'))
		context ['quote_total'] = Quote.objects.aggregate(quote_count=Count('id'))
		context ['rec_total'] = Review.objects.filter(recommend=True).aggregate(rec_count=Count('id'))
		return context

class ChartGenerate(ListView):
	template_name='somesmart/include_charts_generate.html'
	context_object_name = 'chart_data'

	def get_queryset(self):
		chart_name = self.kwargs['chart']
		if self.kwargs['option']:
			option = self.kwargs['option']
		if chart_name == 'PagesByGenre':
			return Review.objects.select_related().values('edition__book__genre__slug').annotate(chart_count=Sum('edition__pages')).order_by()
		elif chart_name == 'BooksByGenre':
			return Review.objects.select_related().values('edition__book__genre__slug').annotate(chart_count=Count('id')).order_by()
		elif chart_name == 'GeekQuotient':
			return Radar.objects.select_related().values('world', 'realism', 'book__edition__review__finished', 'book__title').order_by('book__edition__review__finished')
		elif chart_name == 'GeekHist':
			return Radar.objects.select_related().values('world', 'realism', 'book__title', 'book__edition__review__recommend')
		elif chart_name == 'GenreTransitions':
			return Review.objects.select_related().values('edition__book__genre__id','finished').order_by('finished')
		elif chart_name == 'BookAgeHist':
			return Review.objects.select_related().extra(select={'age_read': "FLOOR(DATEDIFF(finished,original_publication) / 365)", 'title': "title"}).order_by('age_read')
		elif chart_name == 'Timeline':
			return Review.objects.select_related().values('edition__book__title','started','recommend','finished').filter(finished__year=option).order_by('finished')

	def get_context_data(self, **kwargs):
		context = super(ChartGenerate, self).get_context_data(**kwargs)
		chart_name = self.kwargs['chart']
		if chart_name == 'PagesByGenre':
			context ['chart_title'] = "Pages by Genre"
			context ['chart_legend'] = "Pages"
			context ['chart_type'] = "BarChart"
			context ['chart_name'] = chart_name
			return context
		if chart_name == 'BooksByGenre':
			context ['chart_title'] = "Books by Genre"
			context ['chart_legend'] = 'Books'
			context ['chart_type'] = "BarChart"
			context ['chart_name'] = chart_name
			return context
		if chart_name == 'GeekQuotient':
			context ['chart_title'] = "Geek Quotient"
			context ['v_axis'] = 'Geek Quotient'
			context ['chart_type'] = 'SteppedAreaChart'
			context ['chart_name'] = chart_name
			return context
		if chart_name == 'GenreTransitions':
			context ['chart_title'] = "Genre Transitions"
			context ['v_axis'] = 'Genre Transitions'
			context ['chart_type'] = 'SteppedAreaChart'
			context ['chart_name'] = chart_name
			return context
		if chart_name == 'BookAgeHist':
			context ['chart_title'] = 'Book Age When Read'
			context ['chart_type'] = 'Histogram'
			context ['chart_name'] = chart_name
			return context
		if chart_name == 'GeekHist':
			context ['chart_title'] = 'Geek Quotient Spread'
			context ['chart_type'] = 'Histogram'
			context ['chart_name'] = chart_name
			return context
		if chart_name == 'Timeline':
			context ['chart_title'] = 'Reading Timeline by Recommendation'
			context ['chart_type'] = 'Timeline'
			context ['chart_name'] = chart_name
			return context


class QuoteView(DetailView):
	queryset=Quote.objects.select_related()
	template_name='somesmart/base_quote.html'

class QuoteList(ListView):
	queryset=Quote.objects.select_related().values('quote_type__name', 'quote_type__id').annotate(quote_count=Count('id')).order_by()
	template_name='somesmart/base_quote_list.html'
	context_object_name = 'quote_stats'

class QuoteTypeList(ListView):
	template_name='somesmart/base_quote_list.html'
	context_object_name = 'type_list'
	paginate_by = 25

	def get_queryset(self):
		return Quote.objects.filter(quote_type=self.kwargs['type'])

	def get_context_data(self, **kwargs):
		context = super(QuoteTypeList, self).get_context_data(**kwargs)
		context['quote_stats'] = Quote.objects.select_related().values('quote_type__name', 'quote_type__id').annotate(quote_count=Count('id')).order_by()
		return context

class QuoteAuthorList(ListView):
	template_name='somesmart/base_quote_list.html'
	context_object_name = 'search_list'
	paginate_by = 25

	def get_queryset(self):
		return Quote.objects.filter(edition__book__author__id=self.kwargs['author'])

class QuoteBookList(ListView):
	template_name='somesmart/base_quote_list.html'
	context_object_name = 'search_list'
	paginate_by = 25

	def get_queryset(self):
		return Quote.objects.filter(edition__book__id=self.kwargs['book'])

class AuthorView(DetailView):
	queryset=Author.objects.select_related()
	template_name='somesmart/base_author.html'

class ReviewView(DetailView):
	queryset=Review.objects.select_related()
	template_name='somesmart/base_review.html'

class ReviewList(ListView):
	queryset=Review.objects.select_related().order_by('-finished')
	template_name='somesmart/base_review_list.html'
	context_object_name = 'review_list'
	paginate_by = 25

	def get_context_data(self, **kwargs):
		context = super(ReviewList, self).get_context_data(**kwargs)
		context['genre_list'] = Genre.objects.values('name', 'slug').order_by('name')
		return context

class ReviewGenreList(ListView):
	template_name='somesmart/base_review_list.html'
	context_object_name = 'review_list'
	paginate_by = 25

	def get_queryset(self):
		return Review.objects.select_related().filter(edition__book__genre__slug=self.kwargs['genre']).order_by('-finished')

	def get_context_data(self, **kwargs):
		context = super(ReviewGenreList, self).get_context_data(**kwargs)
		context['genre_list'] = Genre.objects.values('name', 'slug').order_by('name')
		context['genre_value'] = Genre.objects.filter(slug=self.kwargs['genre'])
		return context

class ReviewByBook(ListView):
	template_name='somesmart/base_review_list.html'
	context_object_name = 'review_list'
	paginate_by = 25

	def get_queryset(self):
		return Review.objects.select_related().filter(edition__book__id=self.kwargs['pk'])

class ShelfView(DetailView):
	queryset=Shelf.objects.select_related()
	template_name='somesmart/base_shelf.html'

def get_gr_current(request):
	response = urllib.request.urlopen('https://www.goodreads.com/user_status/list/293378-scott-forbes?format=rss')
	gr_xml = response.read()
	#close the file
	response.close()
	dom = parseString(gr_xml)
	#find the second title tag
	xmlTag = dom.getElementsByTagName('title')[1].toxml()
	#get rid of the parts we don't want
	xmlData=xmlTag.replace('<title>','').replace('</title>','').replace('Forbes ', '')
	#find the second link tag and do the same as above
	xmlLink = dom.getElementsByTagName('link')[1].toxml()
	xmlLink=xmlLink.replace('<link>','').replace('</link>','')
	#put it in in a dictionary
	results = [{ 'link': xmlLink, 'status': xmlData }]
	json_results = json.dumps(results)
	if results:
		return HttpResponse(json_results, content_type='application/json')

def get_random_quote(request):
	random = Quote.objects.exclude(quote_type__id=3).exclude(quote_type__id=4).order_by('?')[:1].get()
	return render_to_response('somesmart/include_quote.html', {'quote' : random})

def zinnia_entry_detail(request, year, slug):
	#fixing an annoying typo for legacy urls
	if slug == 'beyond-the-blue-event-horizon-hechee-saga':
		slug = 'beyond-the-blue-event-horizon-heechee-saga'
	elif slug == 'first-line-extremely':
		slug = 'first-line-extremely-loud-and-incredibly-close'
	elif slug == 'how-to-read-literature':
		slug = 'how-to-read-literature-like-a-professor'
	elif slug == 'the-moon-is-a-harsh':
		slug = 'the-moon-is-a-harsh-mistress'
	elif slug == 'of-other':
		slug = 'of-other-worlds-essays-and-stories'

	entry = Entry.published.on_site().get(slug=slug)
	return redirect('zinnia:entry_detail', year=entry.creation_date.strftime('%Y'), month=entry.creation_date.strftime('%m'), day=entry.creation_date.strftime('%d'), slug=entry.slug)
	return render_to_response('zinnia/legacy_entry_detail.html', {'object': entry})

def zinnia_latest_feeds(request):
	return redirect('zinnia_entry_latest_feed')

# ****************************************************************** #
# *********************** favorites views ************************** #
# ****************************************************************** #

class FavoriteList(ListView):
	template_name='somesmart/base_favorite_list.html'
	context_object_name = 'genre_list'

	def get_queryset(self):
		return Favorite.objects.select_related().values('book__genre__slug', 'book__genre__name').distinct()

class FavoriteGenreList(ListView):
	template_name='somesmart/base_favorite_list.html'
	context_object_name = 'favorite_list'
	paginate_by = 5

	def get_queryset(self):
		return Favorite.objects.select_related().filter(book__genre__slug=self.kwargs['genre']).order_by('rank')

	def get_context_data(self, **kwargs):
		context = super(FavoriteGenreList, self).get_context_data(**kwargs)
		context['genre_list'] = Favorite.objects.select_related().values('book__genre__slug', 'book__genre__name').distinct()
		return context

# ****************************************************************** #
# ********************** list related views ************************ #
# ****************************************************************** #

class ListDetailView(DetailView):
	template_name='somesmart/base_list.html'
	queryset = List.objects.order_by('list_name')  

	def get_context_data(self, **kwargs):
		context = super(ListDetailView, self).get_context_data(**kwargs)
		self.list_id = self.kwargs['pk']
		self.list = List.objects.get(id=self.list_id)
		#all the books in the list
		self.book_ids = ListDetail.objects.select_related().filter(list=self.list_id).values('book')
		#all the books in the list that have been read
		self.read_ids = Review.objects.select_related().filter(edition__book__in=self.book_ids).values('edition__book').distinct()
		#all the reads that have been read by the current user
		self.user_read_ids = Review.objects.filter(edition__book__in=self.book_ids, reader=self.list.user).values('edition__book').distinct()
		#all the reads that OTHERS have read, but not those the user has read
		self.others_read_ids = Review.objects.filter(edition__book__in=self.book_ids).exclude(edition__book__in=self.user_read_ids).values('edition__book').distinct()
		#distinct reads from the list the current user has read
		self.distinct_user_read = ListDetail.objects.select_related().filter(book__in=self.user_read_ids, list=self.list_id).order_by('book__title')
		#amount read by the user
		self.total_read_user = len(self.distinct_user_read)
		#count of the list
		self.list_total = len(self.book_ids)
		#pull the books in the list that have been read by the user
		context['user_read'] = self.distinct_user_read	 
		#those read by other users
		context['others_read'] = ListDetail.objects.select_related().filter(book__in=self.others_read_ids, list=self.list_id).order_by('book__title').distinct()
		#those orgs not ever found
		context['never_read'] = ListDetail.objects.select_related().filter(list=self.list_id).exclude(book__in=self.read_ids).distinct().order_by('book__title').distinct()
		#percent complete stats
		getcontext().prec = 2
		context['completion'] = {'total': self.list_total, 'total_user': self.total_read_user}
		return context

class ListSummary(ListView):
	template_name='somesmart/base_list_summary.html'
	context_object_name = 'list_summary'
	def get_queryset(self):
		return List.objects.all()

class ListCreateView(CreateView):
	template_name = 'somesmart/base_list_create.html'
	model = List #Must keep this
	form_class = ListForm

	def form_valid (self, form):
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = self.request.user
			obj.save()
		context = self.get_context_data()
		listdetail_form = context['listdetail_form']
		if listdetail_form.is_valid():
			self.object = form.save()
			listdetail_form.instance = self.object
			listdetail_form.save()
			return HttpResponseRedirect('/list/')
		else:
			return self.render_to_response(self.get_context_data(form=form))

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(ListCreateView, self).get_context_data(**kwargs)
		if self.request.POST:
			context['listdetail_form'] = ListDetailFormSet(self.request.POST, instance=self.object)
		else:
			context['listdetail_form'] = ListDetailFormSet(instance=self.object)
		return context

def delete_list(request, pk):
	list_user = List.objects.select_related().get(id=pk)
	if request.user.id == list_user.user.id:
		List.objects.filter(id=pk).delete()
		return HttpResponse("success")
	else:
		return HttpResponse("you shouldn't be here")

class ListUpdate(UpdateView):
	template_name = 'somesmart/base_list_update.html'
	model = List #Must keep this
	form_class = ListForm

	def form_valid (self, form):
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			return HttpResponseRedirect('/list/')

	def get_context_data(self, **kwargs):
		context = super(ListUpdate, self).get_context_data(**kwargs)
		self.list_id = self.kwargs['pk']
		context['detail_list'] = ListDetail.objects.select_related().filter(list=self.list_id).order_by('book__title')
		return context

def delete_list_item(request, pk):
	list_user = List.objects.select_related().get(list_details__id=pk)
	if request.user.id == list_user.user.id:
		ListDetail.objects.filter(id=pk).delete()
		return HttpResponse("success")
	else:
		return HttpResponse("you shouldn't be here")

def add_list_item(request, list, book):
	list_user = List.objects.select_related().get(id=list)
	book = Book.objects.get(id=book)
	if request.user.id == list_user.user.id:
		new_item = ListDetail(list=list_user, book=book)
		new_item.save()
		return HttpResponse(new_item.id)
	else:
		return HttpResponse("you shouldn't be here")

def copy_list(request, list):
	list = List.objects.get(id=list)
	if list:
		new_user = User.objects.get(id=request.user.id)
		new_list = List(list_name=list.list_name, list_descr=list.list_descr, user=new_user, is_group=False)
		new_list.save()
	list_detail = ListDetail.objects.filter(list=list)
	if list_detail:
		for detail in list_detail:
			new_list_detail = ListDetail(list=new_list, book=detail.book)
			new_list_detail.save()
	return HttpResponseRedirect('/list/')

# ****************************************************************** #
# ********************* tagging related vws ************************ #
# ****************************************************************** #

def book_tags(request, book):
	book = Book.objects.get(id=book)
	tags = Tag.objects.get_for_object(book)

	tag_list = []
	for tag in tags:
		data = {'id': tag.id, 'tag': tag.name}
		tag_list.append(data)

	results = {'tags': tag_list}
	json_results = json.dumps(results)
	return HttpResponse(json_results, content_type='application/json')

def current_tags(request):
	tags = Tag.objects.usage_for_model(Book, counts=True, min_count=None, filters=None)

	tag_list = []
	for tag in tags:
		data = {'id': tag.id, 'tag': tag.name, 'count': tag.count }
		tag_list.append(data)

	results = {'tags': tag_list}
	json_results = json.dumps(results)
	return HttpResponse(json_results, content_type='application/json')

def save_tags(request, book):
	book = Book.objects.get(id=book)
	try:
		Tag.objects.update_tags(book, request.POST['new_tags'])
		return HttpResponse('1')
	except:
		return HttpResponse('0')

class TagListView(ListView):
	template_name='somesmart/base_search_tags.html'
	context_object_name='book_list'
	paginate_by = 9

	def get_queryset(self):
		self.tag = Tag.objects.get(name = self.kwargs['tag'])
		#get the books tagged with this tag
		self.tagged_books = TaggedItem.objects.filter(tag=self.tag).values('object_id')
		return Book.objects.select_related().filter(id__in= self.tagged_books).order_by('title')

def get_related(request, book):
	book = Book.objects.get(id=book)
	related = TaggedItem.objects.get_related(book, Book, num=5)

	related_list = "<ul class='list-unstyled'>"
	for book in related:
		related_list += "<li><a href='/book/" + str(book.id) + "/" + slugify(book.title) + "/'><i class='glyphicon glyphicon-minus'></i> " + book.title + "</a></li>" 

	related_list += "</ul>"
	return HttpResponse(related_list)

def get_cloud(request, min_count):
	tags = Tag.objects.cloud_for_model(Book, steps=1, distribution=LOGARITHMIC,filters=None, min_count=min_count)

	cloud = "<ul class='list-inline'>"
	for tag in tags:
		cloud += "<li><a href='/tags/search/" + tag.name + "/'>" + tag.name + " <span class='badge'>" + str(tag.count) + "</span></a></li>"

	cloud += "</ul>"
	return HttpResponse(cloud)