from django.shortcuts import render, redirect
from .models import Donor, Donate
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from datetime import datetime
from adminpanel.models import Inventory
from volunteer.models import Volunteer
from volunteer.models import DonorReport

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
    return render(request, 'donor/notification.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('donor_login')

def donor_report_view(request):
    reports = DonorReport.objects.select_related('donor').order_by('-created_at')  # optimized query
    return render(request, 'donor/donorReport.html', {'reports': reports})

def my_donation(request):
    donations = Donate.objects.all()
    return render(request, 'donor/myDonation.html', {'donations': donations})
