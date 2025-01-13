from django.urls import path
from . import views

urlpatterns = [
    path('validate/', views.validate, name='validate'),
    path('download_report/', views.download_report, name='download_report'),
]