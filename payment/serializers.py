from rest_framework import serializers
from .models import *

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityReview
        fields = ["id", "user", "booking", 
                  "total_amount", "method", "created_at"]
        extra_kwargs = {"id": {"read_only": True}, "user": {"read_only": True}, 
                        "created_at": {"read_only": True}}
        
    def create(self, validated_data):
        user = self.context.get('user')
        payment = Payment.objects.create(user=user, **validated_data)
        return payment