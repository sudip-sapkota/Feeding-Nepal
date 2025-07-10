from django.core.management.base import BaseCommand
from volunteer.models import Volunteer, HealthCheck, HealthAnalysis
from django.utils import timezone
from django.db import IntegrityError
import random

class Command(BaseCommand):
    help = 'Create random volunteers with health checks'

    def handle(self, *args, **kwargs):
        # Create 5 random volunteers
        for i in range(5):
            full_name = f"Volunteer {i+1}"
            email = f"volunteer{i+1}@example.com"
            mobile = f"123456789{i}"
            dob = timezone.now().date()
            gender = 'Other'
            address = '123 Main St'
            city = 'Kathmandu'
            district = 'Kathmandu'
            password = 'pbkdf2_sha256$150000$nacl$hashedpasswordhere'
            emergency_contact = '9876543210'
            emergency_name = 'Emergency Contact'
            availability = 'Full Time'
            skills = 'Organizing, First Aid'
            terms_accepted = True
            
            try:
                volunteer = Volunteer.objects.create(
                    full_name=full_name,
                    email=email,
                    mobile=mobile,
                    dob=dob,
                    gender=gender,
                    address=address,
                    city=city,
                    district=district,
                    password=password,
                    emergency_contact=emergency_contact,
                    emergency_name=emergency_name,
                    availability=availability,
                    skills=skills,
                    terms_accepted=terms_accepted,
                    created_at=timezone.now()
                )

                # Perform health check
                self.perform_health_check(volunteer)

                self.stdout.write(self.style.SUCCESS(f'Volunteer {full_name} created successfully with health check.'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f'Could not create Volunteer {full_name} due to integrity issues.'))

    def perform_health_check(self, volunteer):
        # Random health data
        temperature = random.uniform(97.0, 99.0)
        heart_rate = random.randint(60, 100)
        blood_pressure_systolic = random.randint(110, 130)
        blood_pressure_diastolic = random.randint(70, 85)
        oxygen_saturation = random.randint(96, 100)
        respiratory_rate = random.randint(12, 20)
        fatigue_level = random.randint(1, 5)
        stress_level = random.randint(1, 5)
        sleep_hours = random.uniform(6.0, 8.0)
        weight = random.uniform(55.0, 75.0)
        height = random.uniform(160.0, 180.0)
        chronic_conditions = False
        covid_symptoms = False

        bmi = weight / ((height / 100) ** 2)

        health_check = HealthCheck.objects.create(
            volunteer_id=volunteer.id,
            volunteer_name=volunteer.full_name,
            volunteer_email=volunteer.email,
            age=25,
            temperature=temperature,
            heart_rate=heart_rate,
            blood_pressure_systolic=blood_pressure_systolic,
            blood_pressure_diastolic=blood_pressure_diastolic,
            oxygen_saturation=oxygen_saturation,
            respiratory_rate=respiratory_rate,
            covid_symptoms=covid_symptoms,
            fatigue_level=fatigue_level,
            stress_level=stress_level,
            sleep_hours=sleep_hours,
            bmi=bmi,
            chronic_conditions=chronic_conditions,
            fitness_level=random.randint(1, 5)
        )

        # Analyze health
        from volunteer.health_analyzer import analyze_health
        analysis_result = analyze_health(health_check)

        HealthAnalysis.objects.create(
            volunteer_id=volunteer.id,
            volunteer_name=volunteer.full_name,
            health_score=analysis_result['score'],
            risk_level=analysis_result['risk_level'],
            work_eligibility=analysis_result['eligibility'],
            analysis_data=analysis_result
        )
        
        self.stdout.write(self.style.SUCCESS(f'Health check and analysis completed for {volunteer.full_name}.'))
