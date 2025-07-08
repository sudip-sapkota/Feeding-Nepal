from django.db import models
from donor.models import Donor  # assuming your donor model is here
from volunteer.models import Volunteer

class Volunteer(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Inventory(models.Model):
    food_type = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    storage_type = models.CharField(max_length=100, blank=True, null=True)
    packaging_type = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collect = models.CharField(max_length=10, default='no')

    def __str__(self):
        return f"{self.food_type} - {self.quantity}"
    class Meta:
        db_table = 'inventory'
        
class Notification(models.Model):
    number = models.CharField(max_length=20)
    gmail = models.CharField(max_length=254)
    role = models.CharField(max_length=20)
    message = models.TextField()
    donor = models.ForeignKey(Donor, null=True, blank=True, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)