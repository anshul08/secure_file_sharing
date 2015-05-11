from django.db import models

class FileLink(models.Model):
	externalName = models.CharField(max_length=200)
	linkSuffix = models.CharField(max_length=200,default='',unique=True)
	created_on = models.DateTimeField('date created')
	password_protected = models.BooleanField(default=False)
	password = models.CharField(max_length = 100)

	class Meta:
		db_table='file_link'