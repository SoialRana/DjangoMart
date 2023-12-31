from django.urls import path
from .import views


urlpatterns = [    
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    
    path('my_orders/',views.my_orders,name='my_orders'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    # path('register/',views.register,name='register'),
    # path('profile/',views.profile,name='profile'),
    # path('login/',views.user_login,name='login'),
    # path('logout/',views.user_logout,name='logout'),
]
