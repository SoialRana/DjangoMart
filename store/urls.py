from django.urls import path
from .import views 

urlpatterns = [
    path('', views.store,name='store'), # jokhon main url er name and path er name same hoye jabe tokhon name dewa jabe na   # jokhon main url er name and path er name same hoye jabe tokhon name dewa jabe na 
    path('category/<slug:category_slug>/', views.store,name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail,name='product_detail'),
    # path('product_detail',views.product_detail,name='product_detail')
]
