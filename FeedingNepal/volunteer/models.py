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
    
    class Meta:
        db_table = 'volunteer'


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
    volunteer_name = models.CharField(max_length=100, blank=True, null=True, help_text="Name of the volunteer who created this report")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report for {self.donor.name} by {self.volunteer_name if self.volunteer_name else 'System'}"
    
    class Meta:
        db_table = 'donorreport'


class VolunteerReport(models.Model):
    # Reports about volunteers created by donors
    volunteer_id = models.IntegerField(help_text="ID of the volunteer being reported")
    volunteer_name = models.CharField(max_length=100, help_text="Name of the volunteer being reported")
    donor_name = models.CharField(max_length=100, blank=True, null=True, help_text="Name of the donor who created this report")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report for {self.volunteer_name} by {self.donor_name if self.donor_name else 'Anonymous'}"
    
    class Meta:
        db_table = 'volunteerreport'


class HealthCheck(models.Model):
    volunteer_id = models.BigIntegerField()  # Matches your DB column name and type
    volunteer_name = models.CharField(max_length=100)
    volunteer_email = models.EmailField(max_length=100, default='')
    age = models.IntegerField()
    temperature = models.FloatField()
    heart_rate = models.IntegerField()
    blood_pressure_systolic = models.IntegerField()
    blood_pressure_diastolic = models.IntegerField()
    oxygen_saturation = models.IntegerField()
    respiratory_rate = models.IntegerField()
    covid_symptoms = models.BooleanField(default=False)
    fatigue_level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    stress_level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    sleep_hours = models.FloatField()
    bmi = models.FloatField()
    chronic_conditions = models.BooleanField(default=False)
    fitness_level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Health Check for {self.volunteer_name} - {self.created_at.date()}"

    class Meta:
        db_table = 'health_check'
        ordering = ['-created_at']


class HealthAnalysis(models.Model):
    volunteer_id = models.BigIntegerField()  # Same logic here
    volunteer_name = models.CharField(max_length=100)
    health_score = models.FloatField()
    risk_level = models.CharField(max_length=20, choices=[
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk')
    ])
    work_eligibility = models.CharField(max_length=20, choices=[
        ('eligible', 'Eligible'),
        ('not_eligible', 'Not Eligible'),
        ('pending', 'Pending Review')
    ], default='pending')
    analysis_data = models.TextField(default='{}')  # Store JSON as text
    created_at = models.DateTimeField(auto_now_add=True)
    admin_decision = models.CharField(max_length=20, choices=[
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending')
    ], default='pending')
    admin_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Health Analysis for {self.volunteer_name} - {self.health_score}"

    class Meta:
        db_table = 'health_analysis'
        ordering = ['-created_at']
