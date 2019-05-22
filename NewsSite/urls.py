from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from . import views


urlpatterns = [
	
	path('', views.index, name="index"),
	path('crawl/<str:forum>', views.crawl, name='crawl'),
	path("filter", views.filter, name='filter'),

]