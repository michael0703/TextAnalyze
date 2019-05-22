"""TextAnalyze URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# -*-coding:utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from loginapp import views as loginviews
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

# admin / weiskewer0703 
# michael0703 / weiskewer0626
# test / aa000000
# Client ID   
# 729760163464-vugpfb80n08l97ak8bi2cbrd7aq554pb.apps.googleusercontent.com
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginviews.index),
    path('index/', loginviews.index),
    path('customdictpage/', include('customdict.urls')),
    path('loginapp/', include('loginapp.urls')),
    path('loginapp/', include('django.contrib.auth.urls')),
    # path('upfile/<str:path>', serve, {"document_root":MEDIA_ROOT}),
    #for google
    path('accounts/', include('allauth.urls')),
    # path('login/', loginviews.login),
    # path('logout/', loginviews.logout),
    # path('register/', loginviews.register),
    path('textmine/', include('textmining.urls')),
    path('uploadArticles/', include('uploadArticle.urls')),
    path('tfidfindex/', include('tfidfanaylze.urls')),
    path('NewsMainpage/', include('NewsSite.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
