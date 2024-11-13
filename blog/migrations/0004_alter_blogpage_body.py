# Generated by Django 4.2.16 on 2024-11-07 00:33
import json

from django.db import migrations
from django.core.serializers.json import DjangoJSONEncoder
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks

def convert_to_streamfield(apps, schema_editor):
    BlogPage = apps.get_model("blog", "BlogPage")
    for page in BlogPage.objects.all():
        page.body = json.dumps(
            [{"type": "rich_text", "value": page.body}],
            cls=DjangoJSONEncoder
        )
        page.save()


def convert_to_richtext(apps, schema_editor):
    BlogPage = apps.get_model("blog", "BlogPage")
    for page in BlogPage.objects.all():
        if page.body:
            stream = json.loads(page.body)
            page.body = "".join([
                child["value"] for child in stream
                if child["type"] == "rich_text"
            ])
            page.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpage_book'),
    ]

    operations = [
        migrations.RunPython(
            convert_to_streamfield,
            convert_to_richtext,
        ),

        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('blockquote', wagtail.blocks.BlockQuoteBlock())]),
        ),
    ]
