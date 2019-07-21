from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import os
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

def get_image_path(instance, filename):
		return os.path.join('photos/ornament', str(instance.year), filename)

class Giver(models.Model):
	first_name = models.TextField(max_length=100)
	last_name = models.TextField(max_length=100)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

class Receiver(models.Model):
	first_name = models.TextField(max_length=100)
	last_name = models.TextField(max_length=100)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

class Ornament(models.Model):
	name = models.TextField(max_length=100)
	slug = models.SlugField(null=True, default=None, blank=True)
	giver = models.ForeignKey(Giver, on_delete=models.CASCADE)
	receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)
	year = models.IntegerField(help_text='The Christmas year the ornament was given')
	notes = models.TextField()
	cloud_location = models.TextField(max_length=250, help_text='The path to the ornament picture in our local cloud storage', null=True, default=None, blank=True)

	image = models.ImageField(upload_to=get_image_path, blank=True)
	image_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(50, 50)], source='image', format='JPEG', options={'quality': 90})
	image_secondary = models.ImageField(upload_to=get_image_path, blank=True)
	image_secondary_thumb = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(50, 50)], source='image', format='JPEG', options={'quality': 90})

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			# Newly created object, so set slug
			self.slug = slugify(self.name)

		super(Ornament, self).save(*args, **kwargs)