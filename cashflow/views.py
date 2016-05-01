from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.db.models import Q, Count, Sum
from django.views.generic import DetailView, ListView, UpdateView, CreateView, FormView
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from cashflow.models import *
from cashflow.forms import TrxForm
from decimal import *
from datetime import datetime, date, timedelta
import urllib2
from xml.dom.minidom import parseString

def success(request):
    return HttpResponse("<p>Trx Created successfully.</p>")

# ****************************************************************** #
# ********************* autocomplete views ************************* #
# ****************************************************************** #

# def autocomplete(request):
# 	if request.method == "GET":
# 		if request.GET.has_key(u'term'):
# 			value = request.GET[u'term']
# 			search = request.GET[u'search']
# 			game = request.GET[u'game']
# 			character = request.GET[u'character']
# 			level = request.GET[u'level']
# 			results = []
# 			if search == "word":
# 				if len(value) > 0:
# 					groups = WordGroup.objects.select_related().values('id').filter(word__word_descr__icontains=value).distinct()
# 					model_results = Story.objects.select_related().filter(wordgroup__id__in=groups, game__id=game, level__id=level, character__id=character)
# 					for word in model_results:
# 						data = {'id': word.wordgroup.id, 'label': word.wordgroup.group_descr }
# 						results.append(data)
# 					json_results = json.dumps(results)
# 					return HttpResponse(json_results, mimetype='application/json')
# 				else:
# 					return HttpResponseRedirect('/noresults/')
# 		else:
# 			return HttpResponseRedirect('/noresults/')

# ****************************************************************** #
# *********************** cashflow views ************************** #
# ****************************************************************** #

class RecentTransactions(ListView):
	template_name='cashflow/base_index.html'
	context_object_name = 'recent_trx'

	def get_queryset(self):
		return Transaction.objects.select_related().order_by('-date')[:10]

def delete_trx(request, pk):
	creator = Transaction.objects.select_related().get(id=pk)
	if request.user.id == creator.budget.creator.id:
		Transaction.objects.filter(id=pk).delete()
		return HttpResponse("success")
	else:
		return HttpResponse("you shouldn't be here")

def add_source(request, name):
	new_source = Source(name=name)
	new_source.save()
	return HttpResponse(new_source.id)

def add_category(request, description):
	new_category = Category(description=description)
	new_category.save()
	return HttpResponse(new_category.id)

class ViewTrx(DetailView):
	queryset=Transaction.objects.select_related()
	template_name='cashflow/base_trx.html'

class AddTrx(CreateView):
	form_class = TrxForm
	model = Transaction
	template_name = 'cashflow/base_add_trx.html'
	def form_valid(self, form):
		if form.is_valid():
			obj = form.save(commit=False)
			self.budget = Budget.objects.select_related().get(id=self.kwargs['pk'])
			if self.request.user.id == self.budget.creator.id:
				obj.save()
				return HttpResponseRedirect("/trx/add/" + str(self.budget) + "/")
			else:
				return HttpResponse("you shouldn't be here")

def first_day_of_month(d):
	return datetime(d.year, d.month, 1, 0, 0, 0)

class ViewForecast(ListView):
	start_date = first_day_of_month(datetime.now())
	end_date = start_date + timedelta(days=90)
	template_name='cashflow/base_forecast.html'
	context_object_name = 'forecast_trx'

	def get_queryset(self):
		return Transaction.objects.select_related().filter(budget=self.kwargs['budget'], date__range=[self.start_date, self.end_date], recurring=False).order_by('date')

	def get_context_data(self, **kwargs):
		context = super(ViewForecast, self).get_context_data(**kwargs)
		self.budget = self.kwargs['budget']
		#current_balance = BudgetAccount.objects.select_related().filter(budget=self.kwargs['budget']).annotate(balance=Sum('account__amount'))
		context['account_balance'] = BudgetAccount.objects.select_related().filter(budget=self.budget)
		context['budget_amounts'] = BudgetDetail.objects.select_related().filter(budget=self.budget)
		recurring_list = []
		trx_recurr = Transaction.objects.filter(recurring=True, budget=self.budget)
		for trx in trx_recurr:
			recurr = Transaction.objects.get(pk=trx.id)
			dates = recurr.recurrences.between(datetime(recurr.date.year, recurr.date.month, recurr.date.day, 0, 0, 0),self.end_date, inc=True)
			for date in dates:
				data = {'date': date.date, 'amount': trx.amount, 'source': trx.source, 'category': trx.category, 'account': trx.account, 'id': trx.id}
				recurring_list.append(data)
		context['recurring_trx'] = recurring_list
		return context
