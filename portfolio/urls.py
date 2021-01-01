
from django.urls import path
from . import views

urlpatterns = [
    path('import/', views.ReportImport.as_view(), name='import_report'),

    path('deals/', views.DealList.as_view(), name='deals'),
    path('deals/create/', views.DealCreate.as_view(), name='deal_create'),

    path('', views.portfolio_stats, name='portfolio'),
]
