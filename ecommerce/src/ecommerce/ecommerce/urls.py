"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path,include


from django.conf.urls.static import static
from django.conf import settings
#from django.views.generic import TemplateView
from carts.views import cart_home

from mysite.views import home_page,contact_page,login_page,about_page,register_page
urlpatterns = [
   #path('',views.home_page ,name="home_page"),

   path('admin/', admin.site.urls),
   #path('bootstrap/',views.TemplateViews.as_view(),name="bootsrtap/example.html"),
   path('',include("mysite.urls")),
   path('search/',include(('search.urls','search'),namespace='search')),
 path('cart/',include(("carts.urls","carts") , namespace='cart')),


]

if settings.DEBUG:
    urlpatterns=urlpatterns+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
