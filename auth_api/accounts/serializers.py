from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'tc', 'password','password2']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self,data):
        password = data.get('password')
        password2 = data.get('password2')
        if password.lower() != password2.lower():
            raise serializers.ValidationError("Password field doesn't match!")
        return data

    def create(self,validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)


    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user= self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and confirm passord field doesn't match")
        user.set_password(password)
        user.save()
        return data

class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, data):
        email = data.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('No email id exist with this email')
        return data


class UserResetPasswordDoneSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    def validate(self,data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm passord field doesn't match")
        return data
