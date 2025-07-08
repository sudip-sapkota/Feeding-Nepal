from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from donor.models import Donate
from django.utils.timezone import now
from datetime import date
from donor.models import Donor
from volunteer.models import Volunteer
from .models import Inventory
from django.utils.dateparse import parse_date
from .models import Notification
from django.contrib.auth import logout
from donor.models import Donate
from donor.models import Donor        
from datetime import date, timedelta





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
    # --- auth guard ---------------------------------------------------------
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    # --- 1. recent & expiring donations -------------------------------------
    recent_donations = Donate.objects.select_related('donor')\
                                     .order_by('-created_at')[:5]

    expiring_items_queryset = Donate.objects.filter(
        expiry_date__isnull=False,
        expiry_date__gte=now().date()
    ).order_by('expiry_date')[:10]

    expiring_soon_items = [
        {
            "food_type":  item.food_type,
            "quantity":   item.quantity,
            "expiry_date": item.expiry_date,
            "days_left":  (item.expiry_date - date.today()).days,
        }
        for item in expiring_items_queryset
    ]

    # --- 2. shared time ranges ----------------------------------------------
    today = now().date()
    this_month_start = today.replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    # --- 3. donor stats -----------------------------------------------------
    total_donors = Donor.objects.count()
    donors_this_month = Donor.objects.filter(
        created_at__date__gte=this_month_start,
        created_at__date__lte=today
    ).count()
    donors_last_month = Donor.objects.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).count()
    raw_donor_growth = (
        (donors_this_month - donors_last_month) * 100 / donors_last_month
        if donors_last_month else (100.0 if donors_this_month else 0.0)
    )
    donor_growth_pct = round(abs(raw_donor_growth), 2)
    donor_growth_direction = "up" if raw_donor_growth >= 0 else "down"

    # --- 4. volunteer stats -------------------------------------------------
    total_volunteers = Volunteer.objects.count()
    volunteers_this_month = Volunteer.objects.filter(
        created_at__date__gte=this_month_start,
        created_at__date__lte=today
    ).count()
    volunteers_last_month = Volunteer.objects.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).count()
    raw_volunteer_growth = (
        (volunteers_this_month - volunteers_last_month) * 100 / volunteers_last_month
        if volunteers_last_month else (100.0 if volunteers_this_month else 0.0)
    )
    volunteer_growth_pct = round(abs(raw_volunteer_growth), 2)
    volunteer_growth_direction = "up" if raw_volunteer_growth >= 0 else "down"

    # --- 5. food donation stats ---------------------------------------------
    total_food_items = Donate.objects.count()
    food_this_month = Donate.objects.filter(
        created_at__date__gte=this_month_start,
        created_at__date__lte=today
    ).count()
    food_last_month = Donate.objects.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).count()
    raw_food_growth = (
        (food_this_month - food_last_month) * 100 / food_last_month
        if food_last_month else (100.0 if food_this_month else 0.0)
    )
    food_growth_pct = round(abs(raw_food_growth), 2)
    food_growth_direction = "up" if raw_food_growth >= 0 else "down"

    # Count expired items
    expired_items_count = Donate.objects.filter(
        expiry_date__isnull=False,
        expiry_date__lt=today
    ).count()

    # --- 6. context ---------------------------------------------------------
    context = {
        "recent_donations":             recent_donations,
        "expiring_soon_items":          expiring_soon_items,

        "total_donors":                 total_donors,
        "donor_growth_pct":             donor_growth_pct,
        "donor_growth_direction":       donor_growth_direction,

        "total_volunteers":             total_volunteers,
        "volunteer_growth_pct":         volunteer_growth_pct,
        "volunteer_growth_direction":   volunteer_growth_direction,

        "total_food_items":             total_food_items,
        "food_growth_pct":              food_growth_pct,
        "food_growth_direction":        food_growth_direction,

        "expired_items_count":          expired_items_count,
    }

    return render(request, "adminpanel/adminIndex.html", context)

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
    notifications = Notification.objects.all().order_by('-created_at')

    enriched_notifications = []
    for n in notifications:
        name = ''
        if n.role == 'donor' and n.donor:
            name = n.donor.name
        elif n.role == 'volunteer' and n.volunteer:
            name = n.volunteer.name
        else:
            name = "Unknown"

        enriched_notifications.append({
            'id': n.id,
            'name': name,
            'number': n.number,
            'role': n.role,
            'message': n.message,
        })

    return render(request, 'adminpanel/adminNotifications.html', {
        'notifications': enriched_notifications
    })

def admin_settings(request):
    return render(request, 'adminpanel/adminSettings.html')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')

def send_notification_page(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        gmail = request.POST.get('gmail')
        role = request.POST.get('role')
        message_text = request.POST.get('message')

        # Create a new Notification object but don't save yet
        notification = Notification(
            number=number,
            gmail=gmail,
            role=role,
            message=message_text,
        )

        # Attach donor or volunteer based on role
        if role == 'donor':
            try:
                donor = Donor.objects.get(email=gmail, phone=number)
                notification.donor = donor
            except Donor.DoesNotExist:
                messages.error(request, "Donor not found.")
                return redirect('send_notification')

        elif role == 'volunteer':
            try:
                volunteer = Volunteer.objects.get(email=gmail, mobile=number)
                notification.volunteer = volunteer
            except Volunteer.DoesNotExist:
                messages.error(request, "Volunteer not found.")
                return redirect('send_notification')

        # Save notification to the database
        notification.save()

        messages.success(request, "Notification sent successfully.")
        return redirect('adminNotifications')  # Adjust the URL name if needed

    return render(request, 'adminpanel/send_notification.html')




def admin_logout(request):
    logout(request)
    return render(request, 'home/index.html')

def delete_item(request, id):
    donation = get_object_or_404(Donate, id=id)
    donation.delete()
    return redirect('admin_donations')  # <-- use the name from urls.py


def delete_item_donor(request, id):
    donor = get_object_or_404(Donor, id=id)
    donor.delete()
    return redirect('admin_donors')




#for edit the inventory
def edit_inventory(request, id):
    inventory = get_object_or_404(Inventory, id=id)
    food_type_options = ["Fresh Produce", "Dairy", "Bakery", "Canned Goods", "Junk Food"]

    if request.method == "POST":
        food_type = request.POST.get("food_type")
        quantity = request.POST.get("quantity")
        storage_type = request.POST.get("storage_type")
        packaging_type = request.POST.get("packaging_type")
        expiry_date = request.POST.get("expiry_date")

        if food_type and quantity:
            inventory.food_type = food_type
            inventory.quantity = quantity
            inventory.storage_type = storage_type
            inventory.packaging_type = packaging_type
            inventory.expiry_date = expiry_date if expiry_date else None
            inventory.save()
            return redirect("admin_inventory")
        else:
            error = "Food type and quantity are required."
            return render(request, "adminpanel/editInventory.html", {
                "inventory": inventory,
                "food_type_options": food_type_options,
                "error": error
            })

    return render(request, "adminpanel/editInventory.html", {
        "inventory": inventory,
        "food_type_options": food_type_options,
    })

def delete_inventory(request, id):
    inventory_item = get_object_or_404(Inventory, id=id)
    inventory_item.delete()
    return redirect('admin_inventory')



# Edit Notification View
def edit_notification(request, id):
    notification = get_object_or_404(Notification, id=id)
    
    if request.method == 'POST':
        number = request.POST.get('number')
        gmail = request.POST.get('gmail')
        role = request.POST.get('role')
        message = request.POST.get('message')

        # Basic validation (optional, extend as needed)
        if not all([number, gmail, role, message]):
            error = "All fields are required."
            return render(request, 'editNotification.html', {
                'notification': notification,
                'error': error,
                'roles': ['donor', 'volunteer'],
            })

        # Update notification fields
        notification.number = number
        notification.gmail = gmail
        notification.role = role
        notification.message = message
        notification.save()

        return redirect('admin_notifications')

    # GET request
    return render(request, 'adminpanel/editNotification.html', {
        'notification': notification,
        'roles': ['donor', 'volunteer'],
    })

# Delete Notification View
def delete_notification(request, id):
    notification = get_object_or_404(Notification, id=id)
    notification.delete()
    return redirect('admin_notifications')