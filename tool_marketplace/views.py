import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework import generics, filters

from authentication.models import CustomUser
from tool_marketplace.filters import ToolFilter
from tool_marketplace.models import Tool, ToolCategory, ToolImage, ToolReceipt
from tool_marketplace.serializers import ToolCategorySerializer, ToolReceiptSerializer, ToolsSerializer

class getTools(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Tool.objects.all()
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ToolFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price_per_unit']

    serializer_class = ToolsSerializer

class createTool(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ToolsSerializer
    queryset = Tool.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        user = CustomUser.objects.get(id=data.get('user_id'))

        # Create the tool instance
        new_tool = Tool.objects.create(
            user_id=user,
            name=data.get('name'),
            description=data.get('description'),
            price_per_unit=data.get('price_per_unit'),
            location_link=data.get('location_link'),
            stock=data.get('stock')
        )

        images = request.FILES.getlist('images')
        for index, image in enumerate(images):
            ToolImage.objects.create(
                tool=new_tool,
                image=image,
                is_primary=(index == 0) 
            )

        categories = request.data.get('category', [])
        if isinstance(categories, str):
            try:
                categories = json.loads(categories)
            except json.JSONDecodeError:
                categories = [categories] 


        for category in categories:
            try:
                category_instance = ToolCategory.objects.get(name=category)
                new_tool.category.add(category_instance)
            except ToolCategory.DoesNotExist:
                print(f"Category not found: {category}")

        new_tool.save()

        serializer = self.get_serializer(new_tool)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class updateDeleteTool(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tool.objects.all()
    serializer_class = ToolsSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Tool.objects.filter(user_id=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Tool successfully deleted.",
            "uuid": kwargs.get('uuid')
        }, status=status.HTTP_200_OK)
    
class getCategories(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = ToolCategory.objects.all()
    serializer_class = ToolCategorySerializer

class buyTool(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ToolReceiptSerializer
    queryset = ToolReceipt.objects.all()

class getReceipts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ToolReceipt.objects.all()
    serializer_class = ToolReceiptSerializer

    filterset_fields = ['user_id', 'tool_id', 'is_paid']

class updateDeleteReceipt(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ToolReceipt.objects.all()
    serializer_class = ToolReceiptSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return ToolReceipt.objects.filter(user_id=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Receipt successfully deleted.",
            "uuid": kwargs.get('uuid')
        }, status=status.HTTP_200_OK)
    