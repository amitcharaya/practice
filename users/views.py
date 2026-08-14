import pyotp

from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.decorators import action
# users/views.py
from rest_framework import viewsets, permissions
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperAdmin
class UserManagementViewSet(viewsets.ModelViewSet):
    # Consider changing this to [permissions.IsAdminUser] in production for safety
    
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated, IsSuperAdmin ]

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({"message": f"User {'enabled' if user.is_active else 'disabled'} successfully."})

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        new_pass = request.data.get('password')
        
        if not new_pass:
            return Response({"error": "Password cannot be empty."}, status=400)
            
        user.set_password(new_pass)
        user.save()
        return Response({"message": "Password reset successfully."})

    # Add the new TOTP reset action
    @action(detail=True, methods=['post'])
    def reset_totp(self, request, pk=None):
        user = self.get_object()
        user.totp_secret = None  # Wipes the secret so the system asks for setup again
        user.save()
        return Response({"message": "2FA reset successfully. The user will be prompted to register a new Authenticator app on their next login."})

    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

