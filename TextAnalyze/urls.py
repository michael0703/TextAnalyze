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
from django.contrib import admin
from django.urls import path, include
from loginapp import views as loginviews



# admin / weiskewer0703 
# michael0703 / weiskewer0626
# test / aa000000
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginviews.index),
    path('index/', loginviews.index),
    path('customdictpage/', include('customdict.urls')),
 	path('register/', loginviews.register),
    path('login/', loginviews.login),
    path('logout/', loginviews.logout),
    path('textmine/', include('textmining.urls')),    

]