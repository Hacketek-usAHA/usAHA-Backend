from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "date_joined"]
        extra_kwargs = {"password": {"write_only": True}, "date_joined": {"read_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class CreateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "date_joined",
                  'first_name', 'last_name', 'bio', 'contact_number', 'profile_pic']
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}, "date_joined": {"read_only": True}}