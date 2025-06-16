from django.db import models
# Remove: from donor.models import Donor


class Volunteer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    dob = models.DateField()
    gender = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    password = models.CharField(max_length=128)  # Store hashed passwords!
    emergency_contact = models.CharField(max_length=20)
    emergency_name = models.CharField(max_length=100)
    availability = models.CharField(max_length=50)
    skills = models.TextField(blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Message(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='messages')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.volunteer.full_name} - {self.subject}"


class DonorReport(models.Model):
    # Use string reference to Donor model
    donor = models.ForeignKey('donor.Donor', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
