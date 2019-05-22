from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [

	path('', views.index, name='tfidfindex'),
	path('tfidf/', views.tfidf, name='dotfidf')
	
	
]