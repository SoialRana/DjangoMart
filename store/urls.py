from django.urls import path
from .import views 

urlpatterns = [
    path('', views.store,name='store'), # when main url name and path name are same this  time we can't use the path name so we can't fill it
    path('category/<slug:category_slug>/', views.store,name='products_by_category'),
    # path('<slug:category_slug>/<slug:product_slug>/', views.product_detail,name='product_detail'),
    # path('product_detail',views.product_detail,name='product_detail')
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]
