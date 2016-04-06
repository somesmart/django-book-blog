from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from cashflow.models import *

class CategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = '__all__'

class TrxForm(ModelForm):
	class Meta:
		model = Transaction
		fields = '__all__'