from django.conf.urls import url
from .views import SearchProductView

urlpatterns=[
   #path('product/',views.product_list_view,name='list'),
   url(r'^$',SearchProductView.as_view(),name='list'),
]
