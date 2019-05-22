from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from loginapp.models import PersonalDict

# Create your models here.
class PersonalDict(models.Model):
	DictName = models.CharField(max_length=20, blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'pds')
	def __str__(self):
		return self.DictName


class UserDictSet(models.Model):
	title = models.CharField(max_length=30, blank=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'DictSet')
	dictset = models.ManyToManyField(PersonalDict)

	def __str__(self):
		return self.title

class UserDictFile(models.Model):
	title = models.CharField(max_length=30, blank=False)
	file = models.FileField(upload_to='UserDictDir/')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'DictFile')

	def __str__(self):
		return self.title

