from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ObtainTokenView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        role = request.data['role']  # Fetch the role from the login form

        try:
            user = User.objects.get(username=username)
            
            # Check the password
            if not user.check_password(password):
                return Response({'detail': 'Invalid password'}, status=400)

            # Check if user has the appropriate role
            if role == 'restaurant' and not hasattr(user, 'restaurant'):
                return Response({'detail': 'No restaurant account found for this user'}, status=400)
            elif role == 'ngo' and not hasattr(user, 'ngo'):
                return Response({'detail': 'No NGO account found for this user'}, status=400)

            # Generate JWT tokens if everything is fine
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        except User.DoesNotExist:
            return Response({'detail': 'Invalid username'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'message': 'This is a protected view'})

def login_view(request):
    return render(request, 'Login.html')

def signup_view(request):
    return render(request, 'Signup.html')

def home_view(request):
    return render(request, 'index.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def new_order_view(request):
    return render(request, 'new_order.html')

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_username(request):
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'available': not exists})

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_email(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'available': not exists})