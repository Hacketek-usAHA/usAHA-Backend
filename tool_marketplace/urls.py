from django.urls import path
from tool_marketplace.views import buyTool, getReceipts, getTools, createTool, getCategories, updateDeleteReceipt, updateDeleteTool

app_name = 'tool_marketplace'

urlpatterns = [
    path('', getTools.as_view(), name='all-tools'),
    path('all-categories/', getCategories.as_view(), name='all-categories'),
    path('create/', createTool.as_view(), name='create-tool'),
    path('buy/<uuid:uuid>/', buyTool.as_view(), name='buy-tool'),
    path('all-receipts/', getReceipts.as_view(), name='all-receipts'),
    path('update-receipt/<uuid:uuid>/', updateDeleteReceipt.as_view(), name='update-payment'),
    path('delete-receipt/<uuid:uuid>/', updateDeleteReceipt.as_view(), name='delete-payment'),
    path('update/<uuid:uuid>/', updateDeleteTool.as_view(), name='update-tool'),
    path('delete/<uuid:uuid>/', updateDeleteTool.as_view(), name='delete-tool'),
]