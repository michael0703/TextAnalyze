from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class UserArticleFile(models.Model):
	title = models.CharField(max_length=30, blank=False)
	file = models.FileField(upload_to='UserArticleDir/')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'ArticleFile')
	hascache = models.BooleanField(default=False)
	cache = models.TextField(default='')
	NerField = models.TextField(default='')

	def __str__(self):
		return self.title

class UserImageFile(models.Model):
	title = models.CharField(max_length=30, blank=False)
	img = models.ImageField(upload_to='UserImgDir/')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'ImgFile')

	def __str__(self):
		return self.title