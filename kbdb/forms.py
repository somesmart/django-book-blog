from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from kbdb.models import *

class LessonForm(ModelForm):
	class Meta:
		model = Lesson
		fields = '__all__'

class LessonRoundForm(ModelForm):
	class Meta:
		model = LessonRound 
		fields = '__all__'

LessonRoundFormSet = inlineformset_factory(Lesson, LessonRound, form=LessonRoundForm)