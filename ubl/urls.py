from django.urls import path
from .views import FileUploadView, UpdateXMLAndConvertToUBLView


urlpatterns = [

    path('ubl/upload/', FileUploadView.as_view(), name='file-upload'),
    path('ubl/update-xml-and-convert/', UpdateXMLAndConvertToUBLView.as_view(), name='update-xml-and-convert'),

]