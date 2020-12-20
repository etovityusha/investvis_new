
from django.urls import path
from . import views

urlpatterns = [
    path('import/', views.ReportImport.as_view(), name='import_report'),
]