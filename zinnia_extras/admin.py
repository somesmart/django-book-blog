from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from zinnia.models import Entry
from zinnia.admin import EntryAdmin

class EntryBookAdmin(EntryAdmin):
	# In our case we put the book field
	# into the 'Content' fieldset
	fieldsets = ((_('Content'), {'fields': (
        'title', 'content', 'image', 'status', 'book')}),) + \
	EntryAdmin.fieldsets[1:]

# Unregister the default EntryAdmin
# then register the EntryBookAdmin class
admin.site.unregister(Entry)
admin.site.register(Entry, EntryBookAdmin)