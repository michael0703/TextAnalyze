from django.db import models
from django.utils.timezone import now
# Create your models here.
class News(models.Model):
	
	title = models.CharField(max_length=100, blank=False)
	timestamp = models.DateField(default=now, editable=True)
	url = models.TextField(default='')
	company = models.CharField(max_length=10, blank=False)
	positiveprob = models.FloatField(blank=False)


	def __str__(self):
		return self.title

# Create your models here.
