from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import datetime
import uuid

class Facility(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="facilities")
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    city = models.CharField(max_length=50)
    location_link = models.TextField(max_length=500)
    price_per_day = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="The price cannot be negative."),]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.images.all().delete()
        self.amenities.all().delete()
        super().delete(*args, **kwargs)
    
{
    "owner": "1dc79cf8-f75b-46d9-afd3-6ec801ba3d09",
    "name": "Dapur Bersama",
    "description": "Dapur bersama untuk bisnis kuliner",
    "city": "Jakarta Timur",
    "location_link": "Jl. Raya Condet, Jakarta Timur",
    "price_per_day": 100000,
    "amenities": [
        {
            "name": "oven",
        },
        {
            "name": "stove",
        }
    ]
}
    
class Facility_Image(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(Facility, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='facility_images/')
    is_primary = models.BooleanField(default=False)
    
class Amenity(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="amenities")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = (('facility_id', 'name'),)

{
    "name": "oven",
}

class Facility_Booking(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="bookings")
    booker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    @property
    def duration(self):
        return (self.end_date - self.start_date).days + 1

    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError("End date cannot be before start date.")
            overlapping_bookings = Facility_Booking.objects.filter(
                facility=self.facility,
                end_date__gte=self.start_date,
                start_date__lte=self.end_date
            ).exclude(id=self.id)
            if overlapping_bookings.exists():
                raise ValidationError("There is already a booking for the specified date range.")

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError("End date cannot be before start date.")
        super(Facility_Booking, self).save(*args, **kwargs)
        self.full_clean()

    def __str__(self):
        return f"Booking by {self.booker} for facility {self.facility} from {self.start_date} to {self.end_date}"


{
    "facility": "11fe80d1-0039-43bb-b5fa-2c3581291ade",
    "booker": "4584d30c-516d-4264-b88f-65ad74b5d917",
    "start_date": "2024-07-21",
    "end_date": "2024-07-21",
    "notes": "Lorem ipsum"
}