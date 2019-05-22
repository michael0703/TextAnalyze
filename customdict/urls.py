from django.contrib import admin
from django.urls import path, include
from . import views

# -*-coding:utf-8 -*-
# admin / weiskewer0703 
# michael0703 / weiskewer0626
# test / aa000000
urlpatterns = [
	path('', views.customdict, name='customdict'),
	path('editdict/', views.editdict, name='editdict'),
	path('editdict/editmsg/<int:idx>', views.edit, name='editpd'),
	path('editdict/deletemsg/<int:idx>', views.delete, name='delpd'),
	path('buildset/', views.build, name='buildset'),
	# path('editset/<int:idx>', views.editset, name='edituds'),
	path('showdictfile/<int:idx>', views.showdictfile, name='showdictfile'),
	path('deletedictfile/<int:idx>', views.deletedictfile, name='deletedictfile'),
]

