from django.urls import path

from . import views


urlpatterns = [
    path('', views.api_overview, name='api_overview'),
    path('stock-list/', views.stock_list, name='stock_list'),
    path('quotes/<str:ticker>/', views.stock_quotes, name='stock_quotes'),
]
