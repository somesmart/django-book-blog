from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from somesmart.models import Book

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('blockquote', blocks.BlockQuoteBlock()),
    ], block_counts={
        'image': {'max_num': 5},
    })

    TYPES = (
        (1, 'Currently Reading'),
        (2, 'Blog Topic'),
    )
    book_type = models.IntegerField(choices=TYPES)

    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('book'),
        FieldPanel('book_type'),
    ]
