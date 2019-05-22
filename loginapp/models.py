from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# class User(AbstractUser):
#     nickname = models.CharField(max_length=30, blank=True)

#     class Meta(AbstractUser.Meta):
#         pass
#     def __str__(self):
#         return self.nickname

class PersonalDict(models.Model):
	DictName = models.CharField(max_length=20, blank=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'pds')
	def __str__(self):
		return self.DictName
