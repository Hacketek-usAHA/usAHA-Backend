from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'contact_number', 'profile_pic']

    def create(self, validated_data):
        user = self.context.get('user')

        if not user:
            raise serializers.ValidationError('User is required')
        
        validated_data.pop('user', None)
        
        profile = Profile.objects.create(user=user, **validated_data)
        return profile