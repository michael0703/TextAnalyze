from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [

	path('', views.index, name='uploadindex'),
	path('adminarticles/', views.admin, name='uploadadmin'),
	path('deletearticle/<int:idx>', views.deletearticle, name='deleteart'),
	path('showarticle/<int:idx>', views.showarticle, name='showart'),
	path('preprocarticleindex/', views.preprocindex, name='preprocindex'),
	path('procarticle/<int:idx>', views.procarticle, name='procarticle'),
	path('showpreprocresult/<int:idx>', views.showpreprocresult, name='showresult'),
	path('uploadimage', views.uploadimage, name='uploadimage'),
	path('uploadimage/admin', views.imgadmin, name='imgadmin'),
	path('uploadimage/delete/<int:idx>', views.deleteimg, name='deleteimg'),
	path('uploadimage/procimg', views.procimg, name='procimg'),
	
]