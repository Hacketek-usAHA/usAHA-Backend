from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
import uuid

class Facility(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="facilities")
    name = models.CharField(max_length=100)
    CATEGORY_CHOICES = [
        ('kitchen', 'Kitchen'),
        ('workshop', 'Workshop'),
        ('art studio', 'Art Studio'),
        ('others', 'Others'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='others')
    description = models.TextField(max_length=500, default="")
    city = models.CharField(max_length=50)
    location_link = models.TextField(max_length=500)
    price_per_day = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="The price cannot be negative."),]
    )
    rating = models.DecimalField(
        default=0,
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0, message="Rating cannot be negative."), 
                    MaxValueValidator(5, message="Rating cannot be more than five")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.images.all().delete()
        self.amenities.all().delete()
        super().delete(*args, **kwargs)
    
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

class Facility_Booking(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="bookings")
    booker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

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
            ).exclude(uuid=self.uuid)
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
    
class FacilityReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    booking = models.OneToOneField(Facility_Booking, on_delete=models.CASCADE, related_name="review")
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Rating cannot be negative."), MaxValueValidator(5, message="Rating cannot be more than five")]
    )
    content = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=FacilityReview)
def update_facility_rating(sender, instance, **kwargs):
    facility = instance.facility
    reviews = FacilityReview.objects.filter(facility=facility)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    facility.rating = round(average_rating, 2) if average_rating is not None else 0
    facility.save()

@receiver(post_delete, sender=FacilityReview)
def update_facility_rating_on_delete(sender, instance, **kwargs):
    facility = instance.facility
    reviews = FacilityReview.objects.filter(facility=facility)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    facility.rating = round(average_rating, 2) if average_rating is not None else 0
    facility.save()