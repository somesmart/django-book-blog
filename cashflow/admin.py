from django.contrib import admin
from django.conf.urls import *
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from cashflow.models import *

class BudgetInline(admin.TabularInline):
	model = BudgetDetail
	extra = 25

class BudgetAdmin(admin.ModelAdmin):
	inlines = [BudgetInline]
	list_display = (
		'name',
		'slug',
		'creator',
		'status',
	)

class TransactionAdmin(admin.ModelAdmin):
	list_display = (
		'date',
		'account',
		'source',
		'category',
		'amount',
	)

class AccountAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'balance',
		'balance_date'
	)

admin.site.register(Budget, BudgetAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Category)
admin.site.register(Source)
admin.site.register(BudgetAccount)
admin.site.register(BudgetDetail)
admin.site.register(Transaction, TransactionAdmin)