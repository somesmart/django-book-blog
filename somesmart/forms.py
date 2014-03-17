from django import forms
from django.forms import ModelForm, Textarea
from django.forms.models import inlineformset_factory
from sssd.somesmart.models import *

# ****************************************************************** #
# ********************* course related forms *********************** #
# ****************************************************************** #

class ListForm(ModelForm):
	list_descr = forms.CharField(widget=forms.TextInput(attrs={'size':'60'}))
		
	class Meta:
		model = List
		exclude = ('user')

	def __init__(self, *args, **kwargs):
		super(ListForm, self).__init__(*args, **kwargs)
		self.fields['list_name'].label = "List Name"
		self.fields['list_descr'].label = "List Description"

class ListDetailForm(ModelForm):
	class Meta:
		model = ListDetail 

ListDetailFormSet = inlineformset_factory(List, ListDetail, form=ListDetailForm)