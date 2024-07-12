from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'contact_number']

    def create(self, validated_data):
        user = self.context.get('user')
        profile = Profile.objects.create(user=user, **validated_data)
        return profile