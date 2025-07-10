from django.shortcuts import render, redirect
from django.db import connection
from django.utils import timezone
from .models import Message
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from donor.models import Donor
from django.shortcuts import render, get_object_or_404, redirect
from adminpanel.models import Inventory, Notification
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import DonorReport, Volunteer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .health_analyzer import analyze_health
from .models import HealthCheck, HealthAnalysis

from donor.models import Donor
# Volunteer Registration View
def volunteer_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender') or None
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        password = request.POST.get('password')
        emergency_contact = request.POST.get('emergencyContact')
        emergency_name = request.POST.get('emergencyName')
        availability = request.POST.get('availability')
        skills = request.POST.get('skills') or None
        terms = request.POST.get('terms')

        # Hash the password
        hashed_password = make_password(password)

        # Insert into database using raw SQL
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO volunteer (
                    full_name, email, mobile, dob, gender, address, city, district,
                    password, emergency_contact, emergency_name, availability,
                    skills, terms_accepted, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                full_name, email, mobile, dob, gender, address, city, district,
                hashed_password, emergency_contact, emergency_name, availability,
                skills, True if terms == 'on' else False, timezone.now()
            ])

        # Store registration data in session and redirect to health check
        request.session['volunteer_reg_email'] = email
        request.session['volunteer_reg_name'] = full_name
        return redirect('check_health')

    return render(request, 'volunteer/register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, password FROM volunteer WHERE email = %s", [email])
            user = cursor.fetchone()

            if user and check_password(password, user[1]):
                request.session['volunteer_email'] = email  # ✅ Save login session
                return redirect('volunteer_index')
            else:
                messages.error(request, "Invalid email or password")

    return render(request, 'volunteer/login.html')

# Volunteer Index View
def index_view(request):
    return render(request, 'volunteer/index.html')

# Example view for volunteer to see available food donations
def food_available(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, donor_id, quantity, food_type, description,
                   pickup_date, pickup_time, storage_type,
                   packaging_type, expiry_date
            FROM donor_donate
            WHERE accepted = 'no'
            ORDER BY created_at DESC
        """)
        donations = cursor.fetchall()

    donation_list = [
        {
            'id': row[0],
            'donor_id': row[1],
            'quantity': row[2],
            'food_type': row[3],
            'description': row[4],
            'pickup_date': row[5],
            'pickup_time': row[6],
            'storage_type': row[7],
            'packaging_type': row[8],
            'expiry_date': row[9],
        }
        for row in donations
    ]

    return render(request, 'volunteer/foodavailable.html', {'donations': donation_list})


def accept_donation(request, donation_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE donor_donate
            SET accepted = 'yes'
            WHERE id = %s
        """, [donation_id])
    return redirect('food_available')

# for the accept 
def accept_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, donor_id, quantity, food_type, description,
                   pickup_date, pickup_time, storage_type,
                   packaging_type, expiry_date
            FROM donate
            WHERE accepted = 'yes'  -- only accepted donations
            ORDER BY created_at DESC
        """)
        donations = cursor.fetchall()

    donation_list = [
        {
            'id': row[0],
            'donor_id': row[1],
            'quantity': row[2],
            'food_type': row[3],
            'description': row[4],
            'pickup_date': row[5],
            'pickup_time': row[6],
            'storage_type': row[7],
            'packaging_type': row[8],
            'expiry_date': row[9],
        }
        for row in donations
    ]

    return render(request, 'volunteer/accept.html', {'donations': donation_list})
# for adding extra fetaurs 

def accept_donation(request, donation_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE donate SET accepted = 'yes' WHERE id = %s
        """, [donation_id])
    return redirect('accept_view')

  # Make sure donor is the correct app name

def donors_tracking(request):
    donors = Donor.objects.all()
    return render(request, 'volunteer/donor-tracking.html', {'donors': donors})


def send_message(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    if request.method == "POST":
        message_text = request.POST.get("message")
        Message.objects.create(
            donor=donor,
            phone=donor.phone,
            email=donor.email,
            message=message_text
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'volunteer/message_form.html', {'donor': donor})


def inventory_view(request):
    inventory = Inventory.objects.all()
    return render(request, 'volunteer/inventory.html', {'inventory': inventory})

def collect_inventory(request, item_id):
    item = get_object_or_404(Inventory, id=item_id)
    if request.method == 'POST':
        # Get the logged-in volunteer
        volunteer_email = request.session.get('volunteer_email')
        if volunteer_email:
            try:
                volunteer = Volunteer.objects.get(email=volunteer_email)
                item.collect = 'yes'
                item.collected_by_name = volunteer.full_name
                item.collected_by_phone = volunteer.mobile
                item.collected_at = timezone.now()
                item.save()
                
                # Create a notification for admin
                from adminpanel.models import Notification
                Notification.objects.create(
                    number=volunteer.mobile,
                    gmail=volunteer.email,
                    role='admin',
                    message=f'Inventory item "{item.food_type}" (ID: {item.id}) has been collected by {volunteer.full_name} ({volunteer.mobile})'
                )
                
            except Volunteer.DoesNotExist:
                # Fallback if volunteer not found
                item.collect = 'yes'
                item.collected_by_name = 'Unknown Volunteer'
                item.collected_by_phone = 'N/A'
                item.collected_at = timezone.now()
                item.save()
        else:
            # No volunteer session
            item.collect = 'yes'
            item.collected_by_name = 'Unknown Volunteer'
            item.collected_by_phone = 'N/A'
            item.collected_at = timezone.now()
            item.save()
            
        collected_items = Inventory.objects.filter(collect='yes')
        return render(request, 'volunteer/collectInventory.html', {'collected_items': collected_items})
    return redirect('inventory')  # fallback redirect if not POST



def donor_report(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO donorreport (donor_id, message, created_at)
                    VALUES (%s, %s, NOW(6))
                    """,
                    [donor.id, message]
                )
            return redirect('success_page')  # Replace with your actual success URL or path

    return render(request, 'volunteer/reportDonor.html', {'donor': donor})


def volunteer_notification_view(request):
    """
    View to display notifications for the logged-in volunteer
    """
    if 'volunteer_email' not in request.session:
        return render(request, 'volunteer/notification.html', {'notifications': []})

    volunteer_email = request.session.get('volunteer_email')
    try:
        volunteer = Volunteer.objects.get(email=volunteer_email)
    except Volunteer.DoesNotExist:
        return render(request, 'volunteer/notification.html', {'notifications': []})

    # Only show notifications specifically for this volunteer
    notifications = Notification.objects.filter(
        role='volunteer',
        volunteer_id=volunteer.id
    )

    notifications = notifications.order_by('-created_at')

    return render(request, 'volunteer/notification.html', {'notifications': notifications})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def volunteer_notification_api(request):
    """
    API endpoint for volunteer notifications
    GET: Retrieve notifications for a specific volunteer
    POST: Create a new notification for a volunteer
    """
    if request.method == 'GET':
        # Extract volunteer_email from session
        volunteer_email = request.session.get('volunteer_email')
        
        if not volunteer_email:
            return JsonResponse({
                'success': False,
                'message': 'Volunteer email is required',
                'notifications': []
            }, status=400)
        
        try:
            volunteer = Volunteer.objects.get(email=volunteer_email)
        except Volunteer.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Volunteer not found',
                'notifications': []
            }, status=404)
        
        # Fetch notifications for this specific volunteer only
        notifications = Notification.objects.filter(
            role='volunteer',
            volunteer_id=volunteer.id
        )
        
        notifications = notifications.order_by('-created_at')
        
        notifications_data = [
            {
                'id': n.id,
                'number': n.number,
                'gmail': n.gmail,
                'message': n.message,
                'created_at': n.created_at.isoformat() if n.created_at else None,
                'volunteer_id': n.volunteer.id if n.volunteer else None,
                'volunteer_name': n.volunteer.full_name if n.volunteer else None
            } for n in notifications
        ]
        
        return JsonResponse({
            'success': True,
            'volunteer_id': volunteer.id,
            'volunteer_name': volunteer.full_name,
            'notifications': notifications_data
        })
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)
        
        volunteer_email = request.session.get('volunteer_email')
        message = data.get('message')
        
        if not volunteer_email or not message:
            return JsonResponse({
                'success': False,
                'message': 'volunteer_email and message are required'
            }, status=400)
        
        try:
            volunteer = Volunteer.objects.get(email=volunteer_email)
        except Volunteer.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Volunteer not found'
            }, status=404)
        
        # Create notification
        notification = Notification.objects.create(
            number=volunteer.mobile,
            gmail=volunteer.email,
            role='volunteer',
            message=message,
            volunteer=volunteer
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Notification created successfully',
            'notification': {
                'id': notification.id,
                'number': notification.number,
                'gmail': notification.gmail,
                'message': notification.message,
                'created_at': notification.created_at.isoformat(),
                'volunteer_id': notification.volunteer.id,
                'volunteer_name': notification.volunteer.full_name
            }
        })


def check_health(request):
    """
    Health check form for newly registered volunteers
    """
    if 'volunteer_reg_email' not in request.session:
        return redirect('volunteer_register')

    if request.method == 'POST':
        try:
            # Get session email
            volunteer_email = request.session['volunteer_reg_email']
            
            # Fetch volunteer from DB using email
            volunteer = Volunteer.objects.get(email=volunteer_email)
            volunteer_id = volunteer.id
            volunteer_name = volunteer.full_name
            
            # Get form data
            temperature = float(request.POST.get('temperature', 98.6))
            heart_rate = int(request.POST.get('heart_rate', 70))
            blood_pressure_systolic = int(request.POST.get('blood_pressure_systolic', 120))
            blood_pressure_diastolic = int(request.POST.get('blood_pressure_diastolic', 80))
            oxygen_saturation = int(request.POST.get('oxygen_saturation', 98))
            respiratory_rate = int(request.POST.get('respiratory_rate', 16))
            fatigue_level = int(request.POST.get('fatigue_level', 1))
            stress_level = int(request.POST.get('stress_level', 1))
            sleep_hours = float(request.POST.get('sleep_hours', 8))
            weight = float(request.POST.get('weight', 70))
            height = float(request.POST.get('height', 170))
            chronic_conditions = request.POST.get('chronic_conditions') == 'on'
            covid_symptoms = request.POST.get('covid_symptoms') == 'on'

            # Calculate BMI
            bmi = weight / ((height / 100) ** 2)

            # Save health check data
            health_check = HealthCheck.objects.create(
                volunteer_id=volunteer_id,
                volunteer_name=volunteer_name,
                volunteer_email=volunteer_email,
                age=25,  # Default age, adjust if you have DOB
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
                fitness_level=5  # Default fitness level
            )

            # Run AI analysis
            analysis_result = analyze_health(health_check)

            # Save analysis result
            HealthAnalysis.objects.create(
                volunteer_id=volunteer_id,
                volunteer_name=volunteer_name,
                health_score=analysis_result['score'],
                risk_level=analysis_result['risk_level'],
                work_eligibility=analysis_result['eligibility'],
                analysis_data=json.dumps(analysis_result)
            )

            # Clear session data
            del request.session['volunteer_reg_email']
            if 'volunteer_reg_name' in request.session:
                del request.session['volunteer_reg_name']

            messages.success(request, "Health check completed! Your application is under review by admin.")
            return redirect('login_view')

        except Volunteer.DoesNotExist:
            messages.error(request, "Volunteer not found.")
            return redirect('volunteer_register')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('check_health')

    return render(request, 'volunteer/checkHealth.html', {
        'volunteer_name': request.session.get('volunteer_reg_name', '')
    })

def handle_notification_response(request):
    """
    Handle volunteer response to admin decision notification
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        volunteer_email = request.POST.get('volunteer_email')
        
        if action == 'approved':
            # Redirect to login page
            messages.success(request, "Welcome! You are now approved to work as a volunteer. Please login to continue.")
            return redirect('login_view')
        elif action == 'rejected':
            # Redirect to registration page
            messages.error(request, "Your application was not approved. Please register again with updated health information.")
            return redirect('volunteer_register')
    
    return redirect('login_view')

def volunteer_report_view(request):
    """
    View for volunteers to see reports about donors, similar to donorReport.html
    """
    # Get the logged-in volunteer's email from session
    volunteer_email = request.session.get('volunteer_email')
    if not volunteer_email:
        messages.error(request, "You must be logged in to view reports.")
        return redirect('login_view')

    # Verify the volunteer exists
    try:
        volunteer = Volunteer.objects.get(email=volunteer_email)
    except Volunteer.DoesNotExist:
        messages.error(request, "Invalid volunteer account.")
        return redirect('login_view')

    # Fetch all donor reports (reports created by this volunteer about donors)
    reports = DonorReport.objects.filter(
        volunteer_name=volunteer.full_name
    ).order_by('-created_at')
    
    context = {
        'reports': [
            {
                'id': report.id,
                'message': report.message,
                'donor_name': report.donor.name if report.donor else 'Unknown',
                'created_at': report.created_at
            }
            for report in reports
        ],
        'volunteer': volunteer,
        'total_reports': reports.count()
    }
    
    return render(request, 'volunteer/volunteerReport.html', context)
