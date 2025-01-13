from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import json
import os
import requests
import base64
import hashlib
from validation.models import Validation
from user.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from django.conf import settings

# Function to get access token from external service
def get_access_token(client_id, client_secret):
    url = 'https://dev-eat.auth.eu-central-1.amazoncognito.com/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'eat/read'
    }
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    return response_data['access_token']

# Function to encode file content to base64 and calculate MD5 checksum
def encode_file(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    base64_content = base64.b64encode(file_content).decode('utf-8')
    md5_checksum = hashlib.md5(base64_content.encode('utf-8')).hexdigest()
    return base64_content, md5_checksum

# Function to validate UBL file using external service
def validate_ubl_file(token, file_path, rules, customer):
    url = 'https://services.ebusiness-cloud.com/ess-schematron/v1/api/validate'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept-Language': 'en'
    }
    base64_content, md5_checksum = encode_file(file_path)
    payload = {
        "filename": file_path.split('/')[-1],
        "content": base64_content,
        "checksum": md5_checksum
    }
    params = {
        'rules': rules,
        'customer': customer
    }
    response = requests.post(url, headers=headers, json=payload, params=params)
    return response.json()

# Function to remove Latin sentences from text
def remove_latin_sentences(text):
    hash_index = text.find('#')
    if hash_index != -1:
        new_text = text[hash_index + 1:]
        return new_text
    return text

# Function to save report as PDF using ReportLab
def save_report_as_pdf(report, file_path):
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    title = Paragraph("Validation Report", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 12))

    summary = Paragraph(f"Summary: {report['summary']}", styles['Normal'])
    content.append(summary)
    content.append(Spacer(1, 12))

    for rule, details in report['reports'].items():
        rule_title = Paragraph(f"Rule: {rule}", styles['Heading2'])
        content.append(rule_title)
        content.append(Spacer(1, 12))

        rule_summary = Paragraph(f"Summary: {details['summary']}", styles['Normal'])
        content.append(rule_summary)
        content.append(Spacer(1, 12))

        if not details['successful']:
            failed_assertions_title = Paragraph("Failed Assertions:", styles['Heading3'])
            content.append(failed_assertions_title)
            content.append(Spacer(1, 12))

            for error in details['firedAssertionErrors']:
                error_text = remove_latin_sentences(error['text'])
                error_details = (
                    f"ID: {error['id']}<br/>"
                    f"Text: {error_text}<br/>"
                    f"Location: {error['location']}<br/>"
                    f"Test: {error['test']}<br/>"
                    f"Flag: {error['flag']}<br/><br/>"
                )
                error_paragraph = Paragraph(error_details, styles['Normal'])
                content.append(error_paragraph)
                content.append(Spacer(1, 12))

    doc.build(content)

# Function to save report as JSON
def save_report_as_json(report, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(report, json_file, indent=4)

# Function to save report as HTML
def save_report_as_html(report, file_path):
    html_content = "<html><head><title>Validation Report</title></head><body>"
    html_content += "<h1>Validation Report</h1>"
    html_content += "<pre>" + json.dumps(report, indent=4, ensure_ascii=False) + "</pre>"
    html_content += "</body></html>"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

# Function to serve file as HTTP response
def serve_file(file_path, file_type):
    with open(file_path, 'rb') as f:
        file_data = f.read()

    response = HttpResponse(file_data, content_type=file_type)
    response['Content-Disposition'] = f'attachment; filename="{file_path.split("/")[-1]}"'
    return response

@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter('rules', openapi.IN_FORM, description="Rules", type=openapi.TYPE_STRING),
        openapi.Parameter('file', openapi.IN_FORM, description="File", type=openapi.TYPE_FILE),
        openapi.Parameter('user_token', openapi.IN_FORM, description="User Token", type=openapi.TYPE_STRING),
    ],
    responses={200: openapi.Response('Success', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'validation_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'original_file_name': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )),
    400: "Invalid request"}
)
@api_view(['POST'])
@csrf_exempt
@parser_classes([MultiPartParser])
@csrf_exempt
def validate(request):
    if request.method == 'POST':
        client_id = '7d30bi87iptegbrf2bp37p42gg'
        client_secret = '880tema3rvh3h63j4nquvgoh0lgts11n09bq8597fgrkvvd62su'
        customer = 'COMPANY'
        rules = json.loads(request.POST.get('rules'))
        file = request.FILES.get('file')
        user_token = request.POST.get('user_token')

        # Ensure all fields are present
        if not all([client_id, client_secret, customer, rules, file, user_token]):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        # Save uploaded file temporarily
        file_path = os.path.join('/tmp', file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        token = get_access_token(client_id, client_secret)
        validation_result = validate_ubl_file(token, file_path, rules, customer)

        os.remove(file_path)  # Clean up the temporary file

        # Save validation result to database
        user = User.objects.get(user_token=user_token)
        validation = Validation(
            user=user,
            valid=validation_result['successful'],
            validation_result=validation_result,
            valid_invoice=file if validation_result['successful'] else None, # Save invoice if validation is successful
        )
        validation.save()

        response_data = validation_result
        response_data['validation_id'] = validation.validation_id
        
        response_data['original_file_name'] = file.name.split('.')[0]  # Include the original file name in the response

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_token': openapi.Schema(type=openapi.TYPE_STRING, description='User Token'),
            'validation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Validation ID'),
            'original_file_name': openapi.Schema(type=openapi.TYPE_STRING, description='Original File Name'),
            'report_format': openapi.Schema(type=openapi.TYPE_STRING, description='Report Format', enum=['pdf', 'json', 'html']),
        }
    ),
    responses={200: 'File download',
               404: "Validation report not found",
               400: "Invalid request"}
)

@api_view(['POST'])
@csrf_exempt
@parser_classes([JSONParser])
def download_report(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_token = data.get('user_token')
        validation_report_id = data.get('validation_id')
        original_file_name = data.get('original_file_name')  # Get the original file name from the request
        report_format = data.get('report_format')

        # Retrieve the validation instance
        try:
            validation = Validation.objects.get(validation_id=validation_report_id, user__user_token=user_token)
        except Validation.DoesNotExist:
            return JsonResponse({'error': 'Validation report not found'}, status=404)

        validation_result = validation.validation_result
        report_path = f"{original_file_name}_report.{report_format}"  # Use the original file name without extension

        if report_format == 'pdf':
            save_report_as_pdf(validation_result['report'], report_path)
        elif report_format == 'json':
            save_report_as_json(validation_result, report_path)
        elif report_format == 'html':
            save_report_as_html(validation_result, report_path)

        with open(report_path, 'rb') as report_file:
            validation.validation_report.save(f"{original_file_name}_report.{report_format}", report_file)

        validation.save()
        os.remove(report_path)  # Clean up the temporary report file

        return serve_file(validation.validation_report.path, 'application/octet-stream')

    return JsonResponse({'error': 'Invalid request'}, status=400)