from django.shortcuts import render, redirect
from django.contrib import messages
from donor.models import Donate
from django.utils.timezone import now
from datetime import date
from donor.models import Donor
from volunteer.models import Volunteer
from .models import Inventory
from django.utils.dateparse import parse_date




def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == 'admin@gmail.com' and password == 'admin123':
            request.session['admin_logged_in'] = True
            return redirect('admin_index')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'adminpanel/admin_login.html')

# Dashboard with recent and expiring donations
def admin_index(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    recent_donations = Donate.objects.select_related('donor').order_by('-created_at')[:5]

    expiring_items_queryset = Donate.objects.filter(
        expiry_date__isnull=False,
        expiry_date__gte=now().date()
    ).order_by('expiry_date')[:10]

    expiring_soon_items = []
    for item in expiring_items_queryset:
        days_left = (item.expiry_date - date.today()).days
        expiring_soon_items.append({
            'food_type': item.food_type,
            'quantity': item.quantity,
            'expiry_date': item.expiry_date,
            'days_left': days_left,
        })

    context = {
        'recent_donations': recent_donations,
        'expiring_soon_items': expiring_soon_items,
    }

    return render(request, 'adminpanel/index.html', context)

# Admin sidebar views
def admin_donors(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    donors = Donor.objects.all()

    donor_data = []
    for donor in donors:
        donations = Donate.objects.filter(donor_id=donor.id).order_by('-created_at')
        total_donations = donations.count()
        last_donation = donations.first().created_at.date() if donations.exists() else None

        donor_data.append({
            'id': donor.id,
            'name': donor.name,
            'email': donor.email,
            'phone': donor.phone,
            'city': donor.city,
            'total_donations': total_donations,
            'last_donation': last_donation,
        })

    return render(request, 'adminpanel/manageDonor.html', {'donor_data': donor_data})



def admin_volunteers(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    volunteers = Volunteer.objects.all().order_by('-created_at')

    volunteer_data = []
    for v in volunteers:
        volunteer_data.append({
            'name': v.full_name,
            'email': v.email,
            'phone': v.mobile,
            'total_collected': 0,  # Dummy data unless you add the field
            'emergency_contact': v.emergency_contact,
        })

    return render(request, 'adminpanel/adminVolunteers.html', {
        'volunteer_data': volunteer_data
    })


def admin_donations(request):
    donations = Donate.objects.select_related('donor').all()
    context = {
        'donations': donations
    }
    return render(request, 'adminpanel/adminDonations.html', context)

def admin_inventory(request):
    # Fetch all inventory items ordered by latest update
    inventory = Inventory.objects.all().order_by('-updated_at')
    
    context = {
        'inventory': inventory,
    }
    
    return render(request, 'adminpanel/adminInventory.html', context)

def update_inventory(request):
    if request.method == 'POST':
        food_type = request.POST.get('food_type')
        quantity = request.POST.get('quantity')
        storage_type = request.POST.get('storage_type', '')
        packaging_type = request.POST.get('packaging_type', '')
        expiry_date = request.POST.get('expiry_date', None)

        # Optional: Validate quantity as integer or handle errors here if needed

        # Convert expiry_date string to date object (if present)
        expiry_date_obj = parse_date(expiry_date) if expiry_date else None

        # Create and save new Inventory record
        Inventory.objects.create(
            food_type=food_type,
            quantity=quantity,
            storage_type=storage_type,
            packaging_type=packaging_type,
            expiry_date=expiry_date_obj
        )



    # For GET request, render empty form or with some defaults if you want
    return render(request, 'adminpanel/updateInventory.html')


def add_data(request):
    # This view is triggered by clicking the "Add" button (link)
    return render(request, 'adminpanel/updateInventory.html')

def admin_apply_food(request):
    return render(request, 'adminpanel/adminApplyFood.html')

def admin_analytics(request):
    return render(request, 'adminpanel/adminAnalytics.html')

def admin_reports(request):
    return render(request, 'adminpanel/adminReports.html')

def admin_notifications(request):
    return render(request, 'adminpanel/adminNotifications.html')

def admin_settings(request):
    return render(request, 'adminpanel/adminSettings.html')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')
