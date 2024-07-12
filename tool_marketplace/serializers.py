from rest_framework import serializers
from .models import Tool, ToolCategory, ToolImage, ToolReceipt


class ToolCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolCategory
        fields = ['name']

class ToolImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolImage
        fields = ['uuid', 'image', 'is_primary', 'tool']

class ToolsSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    images = ToolImageSerializer(many=True, read_only=True)

    class Meta:
        model = Tool
        fields = ['uuid', 'name', 'description', 'price_per_unit', 'location_link', 'stock', 'user_id', 'category', 'images']

    def get_category(self, obj):
        return [category.name for category in obj.category.all()]

class ToolReceiptSerializer(serializers.ModelSerializer):
    receipt_code = serializers.CharField(allow_blank=True, required=False)
    
    class Meta:
        model = ToolReceipt
        fields = '__all__'
