from django.db import models

# Create your models here.
class FileLink(models.Model):
	externalName = models.CharField(max_length=200)
	linkSuffix = models.CharField(max_length=200)
	created_on = models.DateTimeField('date published')
	password_protected = models.BooleanField
	password = models.CharField(max_length = 100)