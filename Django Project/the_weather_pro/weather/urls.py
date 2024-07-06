from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index , name='weather'),  # Named 'weather', used in redirect, reversing urls (in {% url %})
    path('delete/<int:id>/', views.city_delete_view, name='city_delete'),  
    path('list/', views.city_list_view, name='city_list'),  
]