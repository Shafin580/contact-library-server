from django.http import JsonResponse
from rest_framework.response import Response
from .models import Contact, AuthUser
from .serializers import ContactSerializer, AuthUserSerializer
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
import json

# Function to check if a request is valid
def request_validation(request, expectedMethod: str):
    
    # Check if request method is valid
    if request.method != expectedMethod:
        return JsonResponse({'status_code': status.HTTP_405_METHOD_NOT_ALLOWED, 'message': f"Expected a {expectedMethod} request"})

@csrf_exempt
@permission_classes([AllowAny])
# Function to Create Auth User
def createAuthUser(request):
    
    request_validation(request, 'POST')
    
    request_data = json.loads(request.body)
    
    email = request_data["email"]
    password = request_data["password"]

    if not email or not password:
        return JsonResponse({'status_code': status.HTTP_400_BAD_REQUEST, 'message': "Missing/Invalid Email or Password"})

    # Create a new user
    authUser = AuthUser.objects.create(
        email=email,
        username=email,
        password=password,
    )

    # Assign all permissions to the user
    permissions = Permission.objects.all()
    authUser.user_permissions.set(permissions)

    # Generate a JWT token for the user
    token = AccessToken.for_user(authUser)

    # Return a JSON response with the user details and JWT token
    return JsonResponse({
        'status_code': status.HTTP_201_CREATED,
        'user': {
            'id': authUser.id,
            'email': authUser.email,
            'username': authUser.username,
        },
        'token': "Bearer " + str(token),
    })
    
# Function to Authenticate an Auth User
@csrf_exempt
@permission_classes([AllowAny])
def login(request):
    request_validation(request, 'POST')
    
    request_data = json.loads(request.body)
    
    email = request_data["email"]
    password = request_data["password"]

    if not email or not password:
        return JsonResponse({'status_code': status.HTTP_400_BAD_REQUEST, 'message': "Missing/Invalid Email or Password"})

    # Authenticate the user
    # authUser = authenticate(request, email=email, password=password)
    try:
        authUser = AuthUser.objects.get(email=email, password=password)
    except AuthUser.DoesNotExist:
        return JsonResponse({'message': 'Invalid email or password', 'status_code': status.HTTP_401_UNAUTHORIZED})

    # if authUser is None:
    #     return JsonResponse({'message': 'Invalid email or password', 'status_code': status.HTTP_401_UNAUTHORIZED})

    # Generate a JWT token for the user
    token = AccessToken.for_user(authUser)

    # Return a JSON response with the user details and JWT token
    return JsonResponse({
        'status_code': status.HTTP_200_OK,
        'user': {
            'id': authUser.id,
            'email': authUser.email,
            'username': authUser.username,
        },
        'token': "Bearer " + str(token),
    })

# Function to get all contact list
@authentication_classes([IsAuthenticated])
def contact_list(request):
    request_validation(request, 'GET')
    
    # Get all contacts, serialize them and return json
    contacts = Contact.objects.all()
    contactSerializer =  ContactSerializer(contacts,  many=True)  # Serialize the queryset
    
    if contacts:
        return JsonResponse({'status_code': status.HTTP_200_OK, 'results': contactSerializer.data})
    else:
        return JsonResponse({'status_code': status.HTTP_204_NO_CONTENT, 'results': []})

# Function to get single contact details
@authentication_classes([IsAuthenticated])
def contact_detail(request, id):
    
    request_validation(request, 'GET')
    
    # Get single contact, serialize them and return json
    try:
        contactDetail = Contact.objects.get(pk=id)
    except Contact.DoesNotExist:
        return JsonResponse({'status_code': status.HTTP_404_NOT_FOUND, 'results': {}})
    contactSerializer =  ContactSerializer(contactDetail)  # Serialize the queryset
    return JsonResponse({'status_code': status.HTTP_200_OK, 'results': contactSerializer.data})

@authentication_classes([IsAuthenticated])
@csrf_exempt
# Function to add a new contact to database    
def add_contact(request):
    
    request_validation(request, 'POST')
    
    # Add a new contact to database
    request_data = json.loads(request.body)
    contactSerializer = ContactSerializer(data=request_data)
        
    if contactSerializer.is_valid():
        contactSerializer.save()
        return JsonResponse({'status_code': status.HTTP_201_CREATED, 'message': "Data successfully added!"})
    else:
        return JsonResponse({'status_code': status.HTTP_400_BAD_REQUEST, 'message': contactSerializer.errors})

@authentication_classes([IsAuthenticated])    
@csrf_exempt    
# Function to update an existing contact on database    
def update_contact(request, id):
    
    request_validation(request, 'PUT')
    
    # update an existing contact on database
    try:
        contactDetail = Contact.objects.get(pk=id)
    except Contact.DoesNotExist:
        return JsonResponse({'status_code': status.HTTP_404_NOT_FOUND, 'results': {}})
    
    request_data = json.loads(request.body)
    contactSerializer = ContactSerializer(contactDetail, data=request_data)
        
    if contactSerializer.is_valid():
        contactSerializer.save()
        return JsonResponse({'status_code': status.HTTP_200_OK, 'message': "Data successfully updated!"})
    else:
        return JsonResponse({'status_code': status.HTTP_400_BAD_REQUEST, 'message': contactSerializer.errors})

@authentication_classes([IsAuthenticated])
@csrf_exempt
# Function to update an existing contact on database    
def delete_contact(request, id):
    
    request_validation(request, 'DELETE')
    
    # delete an existing contact on database
    try:
        contactDetail = Contact.objects.get(pk=id)
    except Contact.DoesNotExist:
        return JsonResponse({'status_code': status.HTTP_404_NOT_FOUND, 'results': {}})
        
    contactDetail.delete()
    return JsonResponse({'status_code': status.HTTP_200_OK, 'message': "Data successfully deleted!"})