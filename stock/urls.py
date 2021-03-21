from django.urls import path
from . import views

urlpatterns = [
    path('add_company/', views.AddCompany.as_view(), name='company_create'),
    path('<str:ticker>/', views.StockDetail.as_view(), name='ticker'),
    path('newgraph/<str:ticker>/', views.StockDetail2.as_view(), name='ticker'),
    ]
