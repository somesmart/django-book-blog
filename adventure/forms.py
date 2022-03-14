from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from adventure.models import *

class StoryDetailFormset(forms.models.BaseInlineFormSet):
	def __init__(self, *args, **kwargs):
		super(StoryDetailFormset, self).__init__(*args, **kwargs)
		for form in self.forms:
			self.update_choices(form)
	
	# We need to override the constructor (and the associated property) for the
	# empty form, so dynamic forms work.
	@property
	def get_empty_form(self, **kwargs):
		if self.instance is not None:
			form = super(StoryDetailFormset, self).empty_form(parent_instance=self.instance)
			self.update_choices(form)
			return form
	
	# This updates one form's 'character' and 'level' field queryset, if there is a game
	# associated with the formset. Otherwise, make the choice list contain all levels and characters
	def update_choices(self, form):
		if 'game' in self.data:
			characters = Game.objects.get(pk=self.data['game']).character_set.all()
			levels = Game.objects.get(pk=self.data['game']).level_set.all()
		elif self.instance.pk and self.instance.game:
			characters = self.instance.game.character_set.all()
			levels = self.instance.game.level_set.all()
		else:
			characters = Character.objects.all()
			levels = Level.objects.all()
		
		form.fields['character'].queryset = characters
		form.fields['next_level'].queryset = levels

class LevelCharacterFormset(forms.models.BaseInlineFormSet):
	def __init__(self, *args, **kwargs):
		super(LevelCharacterFormset, self).__init__(*args, **kwargs)
		for form in self.forms:
			self.update_choices(form)
	
	@property
	def get_empty_form(self, **kwargs):
		if self.instance is not None:
			form = super(LevelCharacterFormset, self).empty_form(parent_instance=self.instance)
			self.update_choices(form)
			return form
	
	def update_choices(self, form):
		if 'game' in self.data:
			characters = Game.objects.get(pk=self.data['game']).character_set.all()
		elif self.instance.pk and self.instance.game:
			characters = self.instance.game.character_set.all()
		else:
			characters = Character.objects.all()
			levels = Level.objects.all()
		
		form.fields['character'].queryset = characters


class StoryForm(ModelForm):
	class Meta:
		model = Story
		fields = '__all__'

StoryFormSet = inlineformset_factory(Level, Story, form=StoryForm, fk_name='level')