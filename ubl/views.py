import os
import json
import xml.etree.ElementTree as ET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.storage import default_storage
from django.http import HttpResponse
from ubl.serializers import FileUploadSerializer
from .json2ubl_dev.json2ubl_simple import transform_to_ubl, transform_to_xml
from .json2ubl_dev.pdf2ubl import pdf_to_json
from .json2ubl_dev.modify_content import update_xml_content
from validation.validation_rule import validate_input
from user.models import User
from inputdata.models import InputData
from ubl.models import Ubl
from datetime import datetime
from django.core.files.base import ContentFile

class FileUploadView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
       
        file_serializer = FileUploadSerializer(data=request.data)

        if file_serializer.is_valid():
            json_file = request.FILES['json_file']
            file_name = default_storage.save(json_file.name, json_file)
            file_path = os.path.join(default_storage.location, file_name)
            user_token = request.POST.get('user_token')

            ## save input file in database
            user = User.objects.get(user_token=user_token)
            inputData = InputData(
                user_id=user,
                input_content = json_file,
            )
            inputData.save()
         
            try:
                if json_file.name.endswith('.json'): 
                    with open(file_path) as json_file:
                        json_data = json.load(json_file)
                    xml_root = transform_to_xml(json_data)

                    file_name_with_extension = os.path.basename(json_file.name)
                    xml_file_name = os.path.splitext(file_name_with_extension)[0] + '.xml'
                    xml_file_path = os.path.join(default_storage.location, xml_file_name)
                    tree = ET.ElementTree(xml_root)
                    tree.write(xml_file_path, xml_declaration=True, encoding='utf-8', method="xml")
                   
                
                ### pdf
                elif json_file.name.endswith('.pdf'):
                    json_data = pdf_to_json(file_path)
                    new_data_json = json.loads(json_data)
                    xml_root = transform_to_xml(new_data_json)
    
                    xml_file_name = os.path.splitext(json_file.name)[0] + '.xml'
                    xml_file_path = os.path.join(default_storage.location, xml_file_name)
                    tree = ET.ElementTree(xml_root)
                    tree.write(xml_file_path, xml_declaration=True, encoding='utf-8', method="xml")
    
                else:
                    os.remove(file_path)
                    return Response({'message': 'Please upload Json or Pdf.'}, status=status.HTTP_400_BAD_REQUEST)

                validation_result, details = validate_input(xml_file_path)

                # clean file
                os.remove(file_path)
                return Response({'validation_result': validation_result, 'details': details, 'xml_file_name': xml_file_name}, status=status.HTTP_200_OK)
            
            except Exception as e:
                #clean file
                if os.path.exists(file_path):
                    os.remove(file_path)
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateXMLAndConvertToUBLView(APIView):
    def put(self, request, *args, **kwargs):
        updates = request.data.get('updates')
        xml_file_name = request.data.get('xml_file_name')
        user_token = request.data.get('user_token')

        ## check xml_file_name
        if not xml_file_name:
            return Response({'message': 'XML file name is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        xml_file_path = os.path.join(default_storage.location, xml_file_name)

        if not os.path.exists(xml_file_path):
            return Response({'message': 'Original XML file not found.'}, status=status.HTTP_404_NOT_FOUND)
    
        if updates:
            try:
                update_xml_content(xml_file_path, updates)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        validation_result, details = validate_input(xml_file_path)

        if all(validation_result.values()):
 
            ## generate different ubl file
            ubl_dir = os.path.join(default_storage.location, 'uploads/xml')
            os.makedirs(ubl_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

            xml_first_name = os.path.splitext(xml_file_name)[0]
            ubl_file_name = f'{xml_first_name}_ubl_{timestamp}.xml'
            ubl_file_path = os.path.join(ubl_dir, ubl_file_name)
           
            try:
                transform_to_ubl(xml_file_path, ubl_file_path)

                with open(ubl_file_path, 'rb') as f:
                    ubl_content = f.read()
                    response = HttpResponse(ubl_content, content_type='application/xml')
                    response['Content-Disposition'] = f'attachment; filename="{ubl_file_name}"'
                     
                # save ubl in database
                ubl_instance = Ubl(
                    user_id = User.objects.get(user_token=user_token),              
                )
                ubl_instance.ubl_xml.save(ubl_file_name, ContentFile(ubl_content))
                ubl_instance.save()

                #clean temporary files
                os.remove(xml_file_path)
                return response
                
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'validation_result': validation_result, 'details': details, 'xml_file_name':xml_file_name}, status=status.HTTP_400_BAD_REQUEST)