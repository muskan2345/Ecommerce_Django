from django.contrib import admin
from django.conf.urls import url,include
from  mysite import views
from django.urls import path,re_path
#from django.contrib.auth.views import LogoutView
# from django.contrib.auth import views
from mysite.views import ProductListView,ProductDetailView,ProductDetailSlugView,home_page,contact_page,login_page,register_page,guest_register_view

# from views import home_page,about_page,contact_page
urlpatterns = [

     path('',views.home_page,name='home_page' ),
   # url(r'^mysite/',include('mysite.urls')),
    path('about/',views.about_page, name="about_page" ),
      path('contact/',views.contact_page, name="contact" ),
      path('login/',views.login_page,name="login"),
      path('register/guest/',views.guest_register_view,name="guest_register"),
      path('logout/',views.logout_page,name="logout"),
      path('register/',views.register_page,name="register"),
     # path('bootstrap/',views.TemplateViews.as_view(),name="bootsrtap/example.html"),
      # path('product/',views.ProductListView.as_view(),name='list'),
     #path('product/',views.ProductListView.as_view(),name='list'),
    path('product/',views.product_list_view,name='list'),
    path('product/<slug:slug>,<int:pk>/',views.ProductDetailView.as_view(),name='detail'),
    #path('product/,<int:pk>',views.ProductDetailSlugView.as_view(),name='detail'),
    #path('product/<slug:slug>/', views.ProductDetailSlugView.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w\d]+),(?P<id>\d+)/$',views.ProductDetailSlugView.as_view() , name='detail'),

          # path('product/<int:pk>/',views.product_detail_view,name='detail'),

    ##path('product(?P<pk>\d+)/',views.ProductDetailView.as_view(),name='detail'),

]
