
import random
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CustomUserEditForm, ProfilePictureForm

from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect

from django.contrib import messages


from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserCreateSerializer

import json
import requests

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.hashers import make_password

from django.contrib.auth import authenticate, login, logout




# Create your views here.
class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    # Require authentication for this endpoint
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        user = self.get_object(request.user.id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    # Update the user information
    def put(self, request, format=None):
        user = self.request.user

        # Check if email was passed
        email = request.data['email'] if 'email' in request.data else user.email

        # Check if first_name was passed
        first_name = request.data['first_name'] if 'first_name' in request.data else user.first_name

        # Check if last_name was passed
        last_name = request.data['last_name'] if 'last_name' in request.data else user.last_name

        


        updateData = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }

        serializer = CustomUserSerializer(user, data=updateData)
        if serializer.is_valid():
            # Save the serializer
            serializer.save()

            # If an image file is provided, handle it separately
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
                user.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserCreateSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save()#, created_by = self.request.user)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account(request):
    # Try to get the account but if user isn't logged in return an error
    if request.user.is_authenticated:
        account = CustomUser.objects.filter(email__in=[request.user]).first()
        serializer = CustomUserSerializer(account)

        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Optionally, clear all tokens for the user
            user_tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in user_tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        


@require_http_methods(["GET"])
def signup_view(request):
    return render(request, 'signup.html')  # Render the signup form template


# View to handle the account creation
@require_POST
def create_account_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    print(f'Email: {email}, Password: {password}')

    if not email or not password or not first_name or not last_name:
        return JsonResponse({'error': 'All fields are required.'}, status=400)

    # Check if user already exists
    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already in use.'}, status=400)

    # Create new user
    user = CustomUser.objects.create(
        email=email,
        password=make_password(password),
        first_name=first_name,
        last_name=last_name
    )

    return JsonResponse({'success': 'Account created successfully.'})


# View to display the login form
@require_http_methods(["GET"])
def display_login_view(request):
    print(f'request.user: {request.user}')
    if request.user.is_authenticated:
        form = CustomUserEditForm(instance=request.user)
        return render(request, 'profile.html', {'form': form})
    else:
        return render(request, 'login.html')


# View to handle the login form submission
@require_POST
def process_login_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        # Return a special HTMX redirect response
        response = JsonResponse({'redirect': '/accounts/home/'})
        response['HX-Redirect'] = '/accounts/home/'
        return response
    else:
        return JsonResponse({'error': 'Invalid credentials.'}, status=401)
    


@login_required
def home_view(request):
    # The login_required decorator ensures only authenticated users can access this view
    return render(request, 'home.html', {'user': request.user})


@require_POST
def logout_view(request):
    print("HERE")
    logout(request)
    # HTMX expects a JSON response indicating where to redirect.
    response = JsonResponse({'redirect': '/accounts/login/'})
    response['HX-Redirect'] = '/accounts/login/'
    return response
    


@require_POST
def upload_profile_picture(request):
    form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
        # Return the new profile picture URL in the response
        html = '<img src="{}" alt="Profile Picture">'.format(request.user.profile_picture.url)
        return HttpResponse(html)
    else:
        return JsonResponse({'error': form.errors}, status=400)

    



@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return HttpResponse(status=204)  # Or redirect as per your app flow
        else:
            messages.error(request, 'Error updating your profile')
            return redirect('profile')  # Ensure this redirects as intended or handle errors accordingly
    else:
        form = CustomUserEditForm(instance=request.user)
        return render(request, 'profile.html', {'form': form})

    