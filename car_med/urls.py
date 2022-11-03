from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="Home"),
    path('register/', views.get_retail_information, name='ret_info'),
    path('map/', views.map_detail, name='map_detail'),

]
