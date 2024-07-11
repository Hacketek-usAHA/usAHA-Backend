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
    
{
    "username": "user1",
    "password": "password",
    "email": "1111@gmail.com",
    "first_name": "User",
    "last_name": "Satu",
    "bio": "Just a bio",
    "contact_number": "11111111"
}