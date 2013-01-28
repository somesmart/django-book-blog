from django.db import models
from sssd.somesmart.models import Book
from zinnia.models import EntryAbstractClass

class EntryBook(EntryAbstractClass):
    book = models.ForeignKey(Book, null=True, default=None, blank=True)

    def __unicode__(self):
        return 'EntryBook %s' % self.title

    class Meta(EntryAbstractClass.Meta):
        abstract = True