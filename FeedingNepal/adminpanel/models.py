from django.db import models
from donor.models import Donor  # assuming your donor model is here

class Inventory(models.Model):
    food_type = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    storage_type = models.CharField(max_length=100, blank=True, null=True)
    packaging_type = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    collect = models.CharField(max_length=10, default='no')
    collected_by_name = models.CharField(max_length=255, null=True, blank=True)
    collected_by_phone = models.CharField(max_length=20, null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)

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
    volunteer = models.ForeignKey('volunteer.Volunteer', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)