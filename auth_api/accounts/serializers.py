from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password']

        def create(self,validate_data):
            return User.objects.create_user(username=validate_data['username'],email=validate_data['email'],password=validate_data['password'])


