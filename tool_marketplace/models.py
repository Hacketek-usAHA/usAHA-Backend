from django.db import models
from authentication.models import CustomUser
import uuid

class ToolCategory(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tool(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ManyToManyField(ToolCategory, related_name='tools')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_unit = models.IntegerField()
    location_link = models.CharField(max_length=255)
    stock = models.IntegerField()

class ToolImage(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tool = models.ForeignKey('Tool', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tool_images/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.tool.name}"

class ToolReceipt(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tool_id = models.ForeignKey(Tool, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField()
    order_date = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    receipt_code = models.CharField(max_length=255, default='')


