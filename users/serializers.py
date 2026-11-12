## Using Serializers in the User Module
import base64
from io import BytesIO
import pyotp
import qrcode
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from master_data.models import Hotel, SHG






class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # OTP and setup_secret are optional in Step 1, required in Step 2
    otp = serializers.CharField(required=False, write_only=True)
    setup_secret = serializers.CharField(required=False, write_only=True)

    def validate(self, attrs):
        # 1. Validate username and password first (handled by DRF)
        data = super().validate(attrs)
        user = self.user
        otp = attrs.get('otp')
        setup_secret = attrs.get('setup_secret')

        # CASE 1: User already has 2FA configured
        if user.totp_secret:
            if not otp:
                # Step 1: Credentials passed, but OTP is required to proceed
                raise serializers.ValidationError({
                    "error": "otp_required",
                    "detail": "Please enter your Authenticator code."
                })
           
            totp = pyotp.TOTP(user.totp_secret)
            if not totp.verify(otp):
                raise serializers.ValidationError({"detail": "Invalid OTP code."})

        # CASE 2: User needs to setup 2FA
        else:
            if not otp or not setup_secret:
                # Step 1: Generate a secret and QR code, but DO NOT save it to the DB yet
                secret = pyotp.random_base32()
                totp = pyotp.TOTP(secret)
                uri = totp.provisioning_uri(
                    name=user.username,
                    issuer_name="HotelSupplyAPI"
                )

                qr = qrcode.make(uri)
                buffer = BytesIO()
                qr.save(buffer, format="PNG")
                qr_base64 = base64.b64encode(buffer.getvalue()).decode()

                # Tell the frontend to show the QR code and ask for the OTP
                raise serializers.ValidationError({
                    "error": "setup_required",
                    "setup_secret": secret,
                    "qr_code": qr_base64,
                    "detail": "Please scan the QR code and enter the OTP."
                })

            # Step 2: Verify the OTP against the temporary setup_secret
            totp = pyotp.TOTP(setup_secret)
            if not totp.verify(otp):
                raise serializers.ValidationError({"detail": "Invalid OTP code."})

            # ONLY save the secret permanently if verification was successful!
            user.totp_secret = setup_secret
            user.save()

        # 2FA Verified (or Setup complete). Safe to issue tokens.
        data['two_fa_configured'] = True
        data['role'] = user.role
        data['username'] = user.username
        data['hotel_id'] = user.Hotel.id if user.Hotel else None
        data['shg_id'] = user.shg.id if user.shg else None

        return data
   
class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all(), required=False, allow_null=True)
    shg = serializers.PrimaryKeyRelatedField(queryset=SHG.objects.all(), required=False, allow_null=True)
   
    class Meta:
        model = User
        # ADD 'is_active' to this list below:
        fields = ['id', 'username', 'email', 'role', 'hotel', 'shg', 'password', 'is_active']
        read_only_fields = ['id', 'is_active'] # Making is_active read-only is good practice here
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
           
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
