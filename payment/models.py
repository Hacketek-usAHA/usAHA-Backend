from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from facility_rental.models import *
import uuid

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    booking = models.OneToOneField(Facility_Booking, on_delete=models.CASCADE, related_name="payment")
    total_amount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Total amount cannot be negative.")]
    )
    PAYMENT_METHOD_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='debit')
    created_at = models.DateTimeField(auto_now_add=True)
