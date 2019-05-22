from django.contrib import admin
from django.urls import path, include
from . import views 



# admin / weiskewer0703 
# michael0703 / weiskewer0626
# test / aa000000
urlpatterns = [
    path('', views.textmine, name='textmine')
]