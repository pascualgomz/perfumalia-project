from django.urls import path 
from . import views 

urlpatterns = [ 
    path('perfumes/', views.PerfumeList.as_view(), name='perfume_list'),
] 