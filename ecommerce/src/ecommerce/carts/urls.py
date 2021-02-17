from django.contrib import admin
from django.conf.urls import url,include
from  carts import views
from django.urls import path,re_path
from mysite.views import(ProductDetailSlugView)
from .views import(cart_home,cart_update,checkout_home)
urlpatterns=[

      # path('cart/',views.cart_home,name="home"),
      # path('update/',views.cart_update,name="update"),
      url(r'^$',views.cart_home,name='home'),
      url(r'^checkout/$',views.checkout_home,name='checkout'),
      url(r'^update/$',views.cart_update,name='update'),


]
