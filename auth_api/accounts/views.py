from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer ,UserProfileSerializer, UserChangePasswordSerializer, UserResetPasswordSerializer, UserResetPasswordDoneSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import os
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from auth_api.utility import send_email
from django.conf import settings

def get_tokens_for_user(user):
    if not user.is_active:
        raise AuthenticationFailed("User is not active")
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'User registered successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'User login successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email and Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            return Response({'msg':'Password changed successfully'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        serializer = UserResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            user = User.objects.get(email=email)
            if user:
                uid = urlsafe_base64_encode(str(user.id).encode())
                token = PasswordResetTokenGenerator().make_token(user) 
                url = f"http://localhost:3000/api/user/resetpassword/{uid}/{token}"
                print('RESET PASSWORD LINK:- ',url)
                body = f"""
                    Hello {user.name},
                    You requested to reset your password.
                    Click the link below to reset your password:
                    {url}
                    This link is valid for 15 minutes.
                    If you did not request a password reset, please ignore this email.
                    Thanks,
                    Your Team
                    """
                # SEND EMAIL TO USER FOR RESET PASSOWRD
                send_email(address=user.email,subject='RESET PASSWORD',body=body,from_user=settings.DEFAULT_FROM_EMAIL)
                return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User not registered"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserResetPasswordDoneView(APIView):
    permission_classes = [AllowAny]
    def post(self,request,uid,token,format=None):
        serializer = UserResetPasswordDoneSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uid).decode()
                user = User.objects.get(id=uid)
                password = serializer.validated_data.get('password')
                if not PasswordResetTokenGenerator().check_token(user,token):
                    return Response({'error':'Token is not valid or expired'},status=status.HTTP_400_BAD_REQUEST)
                user.set_password(password)
                user.save()
                return Response({'msg':"Password reset successfully"},status=status.HTTP_200_OK)
            except (UnicodeDecodeError,User.DoesNotExist):
                return Response({'error':'Token is not valid or expired'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



