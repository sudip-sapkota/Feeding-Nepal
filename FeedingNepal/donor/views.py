from django.shortcuts import render, redirect
from .models import Donor, Donate
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from datetime import datetime
from adminpanel.models import Inventory
from volunteer.models import Volunteer
from volunteer.models import DonorReport
from adminpanel.models import Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Utility function to create donor reports with volunteer names
def create_donor_report(donor_id, volunteer_name, message):
    """
    Utility function to create a donor report with volunteer information
    """
    try:
        from volunteer.models import DonorReport
        donor = Donor.objects.get(id=donor_id)
        report = DonorReport.objects.create(
            donor=donor,
            volunteer_name=volunteer_name,
            message=message
        )
        return report
    except Exception as e:
        print(f"Error creating donor report: {e}")
        return None

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        address = request.POST.get('address')
        comment = request.POST.get('comment', '')
        password = request.POST.get('password')

        if Donor.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('donor_register')

        try:
            donor = Donor.objects.create(
                name=name,
                email=email,
                phone=phone,
                city=city,
                address=address,
                comment=comment,
                password=make_password(password)
            )
            donor.save()
            messages.success(request, "Registration successful!")
            return redirect('donor_login')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('donor_register')

    return render(request, 'donor/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            donor = Donor.objects.get(email=email)
            if check_password(password, donor.password):
                # Set donor_id in session for context processor usage
                request.session['donor_id'] = donor.id
                messages.success(request, "Login successful!")
                return redirect('index')
            else:
                messages.error(request, "Incorrect password!")
        except Donor.DoesNotExist:
            messages.error(request, "Email not found!")

    return render(request, 'donor/login.html')

def index_view(request):
    # donor is injected globally via context processor, no need to query here
    return render(request, 'donor/index.html')

def make_donation(request):
    if request.method == 'POST':
        donor_id = request.session.get('donor_id')
        if not donor_id:
            messages.error(request, "You must be logged in to make a donation.")
            return redirect('donor_login')

        try:
            donor = Donor.objects.get(id=donor_id)
        except Donor.DoesNotExist:
            messages.error(request, "Donor not found.")
            return redirect('donor_login')

        quantity = request.POST.get('quantity')
        food_type = request.POST.get('food_type')
        description = request.POST.get('description', '')
        pickup_date_str = request.POST.get('pickup_date')
        pickup_time_str = request.POST.get('pickup_time')
        storage_type = request.POST.get('storage_type', '')
        packaging_type = request.POST.get('packaging_type', '')
        expiry_date_str = request.POST.get('expiry_date')

        try:
            pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date() if pickup_date_str else None
            pickup_time = datetime.strptime(pickup_time_str, '%H:%M').time() if pickup_time_str else None
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date() if expiry_date_str else None
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return render(request, 'donor/donation.html')

        Donate.objects.create(
            donor=donor,
            quantity=quantity,
            food_type=food_type,
            description=description,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
            storage_type=storage_type,
            packaging_type=packaging_type,
            expiry_date=expiry_date,
            accepted='no',
            volunteer_id=None
        )

        messages.success(request, "Donation submitted successfully!")
        return redirect('index')

    return render(request, 'donor/donation.html')

def search_volunteers(request):
    districts = Volunteer.objects.values_list('district', flat=True).distinct()
    selected_location = request.GET.get('location', None)

    if selected_location:
        volunteers = Volunteer.objects.filter(district__iexact=selected_location)
    else:
        volunteers = []

    context = {
        'districts': districts,
        'volunteers': volunteers,
        'selected_location': selected_location
    }
    return render(request, 'donor/index.html', context)

def volunteers_tracking_view(request):
    volunteers = Volunteer.objects.all()
    return render(request, 'donor/volunteers_tracking.html', {'volunteers': volunteers})

def inventory_view(request):
    inventory = Inventory.objects.all().order_by('-updated_at')
    context = {
        'inventory': inventory,
    }
    return render(request, 'donor/inventory.html', context)

def analytic_view(request):
    return render(request, 'donor/analytic.html')

def notification_view(request):
    if 'donor_id' not in request.session:
        return render(request, 'donor/notification.html', {'notifications': []})

    donor_id = request.session.get('donor_id')
    try:
        donor = Donor.objects.get(id=donor_id)
    except Donor.DoesNotExist:
        return render(request, 'donor/notification.html', {'notifications': []})

    # Only show notifications specifically for this donor
    notifications = Notification.objects.filter(
        role='donor',
        donor_id=donor.id
    )

    notifications = notifications.order_by('-created_at')

    return render(request, 'donor/notification.html', {'notifications': notifications})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def notification_api(request):
    """
    API endpoint for notifications that matches donor login ID
    GET: Retrieve notifications for a specific donor
    POST: Create a new notification for a donor
    """
    if request.method == 'GET':
        # Extract donor_id from query parameters or session
        donor_id = request.GET.get('donor_id') or request.session.get('donor_id')
        
        if not donor_id:
            return JsonResponse({
                'success': False,
                'message': 'Donor ID is required',
                'notifications': []
            }, status=400)
        
        try:
            donor = Donor.objects.get(id=donor_id)
        except Donor.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Donor not found',
                'notifications': []
            }, status=404)
        
        # Fetch notifications for this specific donor only
        notifications = Notification.objects.filter(
            role='donor',
            donor_id=donor.id
        )
        
        notifications = notifications.order_by('-created_at')
        
        notifications_data = [
            {
                'id': n.id,
                'number': n.number,
                'gmail': n.gmail,
                'message': n.message,
                'created_at': n.created_at.isoformat() if n.created_at else None,
                'donor_id': n.donor.id if n.donor else None,
                'donor_name': n.donor.name if n.donor else None
            } for n in notifications
        ]
        
        return JsonResponse({
            'success': True,
            'donor_id': donor.id,
            'donor_name': donor.name,
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
        
        donor_id = data.get('donor_id') or request.session.get('donor_id')
        message = data.get('message')
        
        if not donor_id or not message:
            return JsonResponse({
                'success': False,
                'message': 'donor_id and message are required'
            }, status=400)
        
        try:
            donor = Donor.objects.get(id=donor_id)
        except Donor.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Donor not found'
            }, status=404)
        
        # Create notification
        notification = Notification.objects.create(
            number=donor.phone,
            gmail=donor.email,
            role='donor',
            message=message,
            donor=donor
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
                'donor_id': notification.donor.id,
                'donor_name': notification.donor.name
            }
        })

def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('donor_login')


def donor_report_view(request):
    """
    View to display donor reports with security check: login_id == donor_id
    Only the logged-in donor can see their own reports
    """
    # Get the logged-in donor's ID from session (this is our login_id)
    login_id = request.session.get('donor_id')
    if not login_id:
        messages.error(request, "You must be logged in to view reports.")
        return redirect('donor_login')

    # Verify the donor exists
    try:
        donor = Donor.objects.get(id=login_id)
    except Donor.DoesNotExist:
        messages.error(request, "Invalid donor account.")
        return redirect('donor_login')

    # Security check: only fetch reports where donor_id matches login_id
    # This ensures login_id == donor_id as requested
    reports = DonorReport.objects.filter(
        donor_id=login_id  # Using donor_id directly for explicit matching
    ).order_by('-created_at')
    
    context = {
        'reports': [
            {
                'id': report.id,
                'message': report.message,
                'volunteer_name': report.volunteer_name or 'Not assigned',
                'created_at': report.created_at
            }
            for report in reports
        ],
        'donor': donor,
        'total_reports': reports.count()
    }
    
    return render(request, 'donor/donorReport.html', context)

def my_donation(request):
    donations = Donate.objects.all()
    return render(request, 'donor/myDonation.html', {'donations': donations})

@csrf_exempt
@require_http_methods(["POST"])
def report_volunteer(request):
    """
    Handle volunteer reporting by donors
    """
    try:
        # Check if donor is logged in
        donor_id = request.session.get('donor_id')
        if not donor_id:
            return JsonResponse({
                'success': False,
                'message': 'You must be logged in to submit a report.'
            }, status=401)
        
        # Get donor information
        try:
            donor = Donor.objects.get(id=donor_id)
        except Donor.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid donor account.'
            }, status=404)
        
        # Get form data
        volunteer_id = request.POST.get('volunteer_id')
        volunteer_name = request.POST.get('volunteer_name')
        message = request.POST.get('message')
        
        if not all([volunteer_id, volunteer_name, message]):
            return JsonResponse({
                'success': False,
                'message': 'All fields are required.'
            }, status=400)
        
        # Create volunteer report
        from volunteer.models import VolunteerReport
        report = VolunteerReport.objects.create(
            volunteer_id=volunteer_id,
            volunteer_name=volunteer_name,
            donor_name=donor.name,
            message=message
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Report submitted successfully!',
            'report_id': report.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)
