from django.urls import path
from . import views

urlpatterns = [
    path('send-file-email/', views.handle_file_email, name='send_file_email'),
    path('handle_xml_file_path_email/', views.handle_xml_file_path_email, name='handle_xml_file_path_email'),
]