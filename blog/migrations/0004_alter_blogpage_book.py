# Generated by Django 4.2.16 on 2024-11-05 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('somesmart', '__first__'),
        ('blog', '0003_blogpage_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='somesmart.book'),
        ),
    ]