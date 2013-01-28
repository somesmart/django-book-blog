from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.db.models import Q, Count
from django.views.generic import DetailView, ListView, UpdateView, CreateView, FormView
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
# from tagging.models import Tag, TaggedItem
from sssd.somesmart.models import *
from zinnia.models import Entry
#from sssd.somesmart.forms import *
from decimal import *
from datetime import datetime
import urllib2
from xml.dom.minidom import parseString

# ****************************************************************** #
# ********************* autocomplete views ************************* #
# ****************************************************************** #

def autocomplete(request):
    if request.method == "GET":
        if request.GET.has_key(u'term'):
            value = request.GET[u'term']
            search = request.GET[u'search']            
            if search == "title":
                # Ignore queries shorter than length 3
                if len(value) > 2:
                    model_results = Book.objects.filter(title__icontains=value)
                    # Default return list
                    results = []
                    for book in model_results:
                        data = {'id': book.id, 'label': book.title }
                        results.append(data)
            elif search == "primary_search":
                if len(value) > 3:
                    model_results = Book.objects.select_related().filter(Q(title__icontains=value) | Q(author__last_name__icontains=value) | Q(author__first_name__icontains=value))
                    results = []
                    data = None
                    for book in model_results:
                        try:
                            data = {'id': '/book/' + str(book.id) + '/' + slugify(book.title) + '/', 'label': book.title }
                        except:
                            data = {'id': '/author/' + str(book.author.id) + '/', 'label': book.author.first_name + ' ' + book.author.last_name }                             
                        results.append(data)
            elif search == "author":
                # Ignore queries shorter than length 4
                if len(value) > 3:
                    model_results = Author.objects.filter(Q(last_name__icontains=value) | Q(first_name__icontains=value))
                    # Default return list
                    results = []
                    for author in model_results:
                        data = {'id': author.id, 'label': author.first_name + ' ' + author.last_name }
                        results.append(data)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

class BookView(DetailView):
    queryset=Book.objects.select_related()
    template_name='somesmart/base_book.html'

def bookinfo_php(request):
    isbn = request.GET[u'bookid']
    book = Book.objects.select_related().get(edition__isbn=isbn)
    return redirect('book-view', pk=book.id)

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
    response = urllib2.urlopen('http://www.goodreads.com/user_status/list/293378-scott-forbes?format=rss')
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
    json = simplejson.dumps(results)
    if results:
        return HttpResponse(json, mimetype='application/json')

def get_random_quote(request):
    random = Quote.objects.exclude(quote_type__id=3).exclude(quote_type__id=4).order_by('?')[:1].get()
    return render_to_response('somesmart/include_quote.html', {'quote' : random})

def zinnia_entry_detail(request, year, slug):
    entry = Entry.published.on_site().get(slug=slug)
    return redirect('zinnia_entry_detail', year=entry.creation_date.strftime('%Y'), month=entry.creation_date.strftime('%m'), day=entry.creation_date.strftime('%d'), slug=entry.slug)
    #return render_to_response('zinnia/legacy_entry_detail.html', {'object': entry})

def zinnia_latest_feeds(request):
    return redirect('zinnia_entry_latest_feed')