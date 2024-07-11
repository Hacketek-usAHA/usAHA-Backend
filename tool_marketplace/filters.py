from django_filters import rest_framework as filters
from .models import Tool

class ToolFilter(filters.FilterSet):
    category = filters.CharFilter(method='filter_by_category')

    class Meta:
        model = Tool
        fields = ['user_id', 'uuid', 'price_per_unit', 'category']

    def filter_by_category(self, queryset, name, value):
        return queryset.filter(category__name=value)
