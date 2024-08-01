from django.urls import path
from .views import *

urlpatterns = [
    path('', PaymentsListAPIView.as_view(), name='payments'),
    path('create/', CreatePaymentAPIView.as_view(), name='create-payment'),
    path('<uuid:pk>/', PaymentDetailAPIView.as_view(), name='payment'),
]