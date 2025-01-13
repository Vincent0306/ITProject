import json
import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from user.models import User
from validation.models import Validation


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'file': openapi.Schema(type=openapi.TYPE_FILE, description='File to send (PDF, JSON, or HTML)'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Recipient email address'),
        },
        required=['file', 'email']
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="File sent successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        status.HTTP_400_BAD_REQUEST: "Bad request",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error"
    }
)
@api_view(['POST'])
def handle_file_email(request):
    file = request.FILES.get('file')
    email = request.POST.get('email')

    if not file or not email:
        return Response({'error': 'Missing file or email address'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Determine file type
        file_type = file.content_type
        file_name = file.name

        # Create EmailMessage object
        email_message = EmailMessage(
            subject='Report Sent',
            body='Please find the attached file.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )

        # Process based on file type
        if file_type == 'application/pdf':
            # PDF file directly attached
            email_message.attach(file_name, file.read(), file_type)
        elif file_type in ['application/json', 'text/html']:
            # JSON and HTML file content read and formatted
            content = file.read().decode('utf-8')
            if file_type == 'application/json':
                # Format JSON
                content = json.dumps(json.loads(content), indent=2)
            email_message.attach(file_name, content, file_type)
        else:
            return Response({'error': 'Unsupported file type'}, status=status.HTTP_400_BAD_REQUEST)

        # Send email
        email_message.send()

        return Response({'message': f'{file_name} has been successfully sent to the specified email'},
                        status=status.HTTP_200_OK)
    except Exception as e:
        # Log error
        print(f"Error sending email: {str(e)}")
        return Response({'error': 'An error occurred while sending the email'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['validation_id', 'email', 'user_token'],
        properties={
            'validation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Validation ID'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Recipient email address'),
            'user_token': openapi.Schema(type=openapi.TYPE_STRING, description='User token'),
        },
    ),
    responses={
        200: 'XML file processed successfully and email sent',
        400: 'Bad Request',
        404: 'File not found',
        500: 'Internal server error'
    }
)

@api_view(['POST'])
def handle_xml_file_path_email(request):
    validation_id = request.data.get('validation_id')
    email = request.data.get('email')
    user_token = request.data.get('user_token')
    print(f"Received validation_id: {validation_id}, email: {email}, user_token: {user_token}")

    if not validation_id or not email or not user_token:
        return Response({'error': 'Missing validation_id, email, or user_token'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the Validation object
        user = User.objects.get(user_token=user_token)
        validation = Validation.objects.get(validation_id=validation_id, user=user)
        valid_invoice = validation.valid_invoice

        if not valid_invoice:
            return Response({'error': 'Valid invoice not found'}, status=status.HTTP_404_NOT_FOUND)

        # Construct the full file path
        full_file_path = valid_invoice.path
        print(f"Attempting to access file: {full_file_path}")

        if not os.path.exists(full_file_path):
            print(f"File not found: {full_file_path}")
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create email
        subject = 'UBL File Attachment'
        body = 'Please find the attached UBL file.'
        from_email = '9900h16a@gmail.com'  # Replace with your sender email
        to_email = [email]

        # Create EmailMessage object
        email_message = EmailMessage(subject, body, from_email, to_email)

        # Add XML file as attachment
        with open(full_file_path, 'rb') as file:
            email_message.attach(os.path.basename(full_file_path), file.read(), 'application/xml')

        # Send email
        email_message.send()

        return Response({'message': 'XML file successfully sent as attachment'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Validation.DoesNotExist:
        return Response({'error': 'Validation not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error sending email with attachment: {str(e)}")
        return Response({'error': f'Error sending email with attachment: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)