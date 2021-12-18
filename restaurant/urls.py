from django.urls import path, include
from .views import *

urlpatterns = [

    path('get-restaurant/', RestaurantView.as_view(), name="get_res"),
    path('add-restaurant/', RestaurantView.as_view(), name="post_res"),
    path('search-restaurant/<str:query>/', search_restaurant, name="search_res"),
    path('filter-restaurant/<str:query>/', filter_restaurant, name="filter_res"),
    path('get-cuisines/', get_cuisines, name="get_cui"),
    path("query/<str:search>/<str:filter>/" , query, name = "query"),
    path('sort-restaurant/<str:order>/<str:query>', sort_restaurant, name="sort_res"),



]