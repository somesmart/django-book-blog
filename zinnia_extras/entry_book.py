from django.db import models
from sssd.somesmart.models import Book
from zinnia.models.entry import EntryAbstractClass

class EntryBook(EntryAbstractClass):
    book = models.ForeignKey(Book, null=True, default=None, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return 'EntryBook %s' % self.title

    class Meta(EntryAbstractClass.Meta):
        abstract = True