import uuid
import re
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def is_valid_email(email):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
        },
    ),
    responses={201: 'Registration successful', 400: 'Bad Request'}
)
@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Both email and password are required'}, status=400)

    if not is_valid_email(email):
        return Response({'error': 'Invalid email format'}, status=400)

    if len(password.strip()) == 0:
        return Response({'error': 'Password cannot be empty'}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=400)

    user = User.objects.create(
        email=email,
        password=make_password(password),
        user_token=uuid.uuid4().hex
    )

    login(request, user)
    return Response({'message': 'Registration successful'}, status=201)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
        },
    ),
    responses={200: 'Login successful', 400: 'Bad Request'}
)
@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Both email and password are required'}, status=400)

    if not is_valid_email(email):
        return Response({'error': 'Invalid email format'}, status=400)

    if len(password.strip()) == 0:
        return Response({'error': 'Password cannot be empty'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email or password'}, status=400)

    if check_password(password, user.password):
        return Response({
            'message': 'Login successful',
            'user_id': user.user_id,
            'email': user.email,
            'token': user.user_token
        })
    else:
        return Response({'error': 'Invalid email or password'}, status=400)

@api_view(['GET'])
def test_api(request):
    return Response({'message': "I'm running!"})