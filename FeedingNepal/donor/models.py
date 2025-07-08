from django.db import models
# Remove: from volunteer.models import Volunteer


class Donor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.TextField()
    comment = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Donate(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)
    food_type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    storage_type = models.CharField(max_length=100, null=True, blank=True)
    packaging_type = models.CharField(max_length=100, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Use string reference to Volunteer model instead of importing it directly
    volunteer = models.ForeignKey('volunteer.Volunteer', on_delete=models.SET_NULL, null=True, blank=True)
    accepted = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')

    def __str__(self):
        return f"{self.food_type} - {self.quantity}"
