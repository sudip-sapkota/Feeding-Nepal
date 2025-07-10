from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
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
import json
from django.db.models import Count, Q, Sum, F
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
    from volunteer.models import HealthAnalysis

    volunteer_data = []
    for v in volunteers:
        # Check if volunteer has health analysis
        try:
            health_analysis = HealthAnalysis.objects.filter(
                volunteer_name=v.full_name
            ).latest('created_at')
            health_status = health_analysis.admin_decision
            health_score = health_analysis.health_score
            work_eligibility = health_analysis.work_eligibility
            has_health_data = True
        except HealthAnalysis.DoesNotExist:
            health_status = 'no_data'
            health_score = None
            work_eligibility = 'unknown'
            has_health_data = False
        
        volunteer_data.append({
            'name': v.full_name,
            'email': v.email,
            'phone': v.mobile,
            'total_collected': 0,  # Dummy data unless you add the field
            'emergency_contact': v.emergency_contact,
            'health_status': health_status,
            'health_score': health_score,
            'work_eligibility': work_eligibility,
            'has_health_data': has_health_data
        })

    return render(request, 'adminpanel/adminVolunteers.html', {
        'volunteer_data': volunteer_data
    })


def admin_delete_volunteer(request, volunteer_email):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    if request.method == 'POST':
        try:
            volunteer = Volunteer.objects.get(email=volunteer_email)
            volunteer.delete()
            messages.success(request, 'Volunteer deleted successfully.')
        except Volunteer.DoesNotExist:
            messages.error(request, 'Volunteer not found.')
    return redirect('admin_volunteers')


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
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    # Basic counts
    total_donations = Donate.objects.count()
    total_volunteers = Volunteer.objects.count()
    total_inventory = Inventory.objects.count()
    total_collected = Inventory.objects.filter(collect='yes').count()
    total_donors = Donor.objects.count()
    total_notifications = Notification.objects.count()

    # Calculate growth percentages
    today = now().date()
    this_month_start = today.replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    donations_this_month = Donate.objects.filter(
        created_at__date__gte=this_month_start,
        created_at__date__lte=today
    ).count()

    donations_last_month = Donate.objects.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).count()

    donations_growth = (
        ((donations_this_month - donations_last_month) * 100 / donations_last_month)
        if donations_last_month else (100.0 if donations_this_month else 0.0)
    )

    volunteers_this_month = Volunteer.objects.filter(
        created_at__date__gte=this_month_start,
        created_at__date__lte=today
    ).count()

    volunteers_last_month = Volunteer.objects.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).count()

    volunteers_growth = (
        ((volunteers_this_month - volunteers_last_month) * 100 / volunteers_last_month)
        if volunteers_last_month else (100.0 if volunteers_this_month else 0.0)
    )

    # Monthly data for chart (last 12 months)
    monthly_data = []
    for i in range(11, -1, -1):
        temp_date = today.replace(day=15) - timedelta(days=30 * i)
        month_start = temp_date.replace(day=1)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)

        monthly_donations = Donate.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end
        ).count()

        monthly_donors = Donor.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end
        ).count()

        monthly_volunteers = Volunteer.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end
        ).count()

        monthly_data.append({
            'month': month_start.strftime('%b'),
            'year': month_start.year,
            'donations': monthly_donations,
            'donors': monthly_donors,
            'volunteers': monthly_volunteers
        })

    # Top donor cities
    top_donors_by_location = Donor.objects.values('city').annotate(
        donor_count=Count('id'),
        total_donations=Count('donate')
    ).filter(total_donations__gt=0).order_by('-total_donations')[:5]

    donor_location_data = []
    for location in top_donors_by_location:
        city_top_donors = Donor.objects.filter(city=location['city']).annotate(
            donation_count=Count('donate')
        ).order_by('-donation_count')[:3]

        donors_info = [{
            'name': donor.name,
            'donations': donor.donation_count,
            'phone': donor.phone
        } for donor in city_top_donors]

        donor_location_data.append({
            'name': location['city'] or 'Unknown',
            'count': location['donor_count'],
            'total_donations': location['total_donations'],
            'top_donors': donors_info
        })

    # Volunteers near top donor cities
    donor_cities = [loc['name'] for loc in donor_location_data]
    volunteer_location_data = []

    for city in donor_cities:
        city_volunteers = Volunteer.objects.filter(city=city)
        volunteer_count = city_volunteers.count()

        if volunteer_count > 0:
            top_volunteers_in_city = []
            for volunteer in city_volunteers[:3]:
                collections = Inventory.objects.filter(
                    collected_by_name=volunteer.full_name,
                    collect='yes'
                ).count()

                top_volunteers_in_city.append({
                    'name': volunteer.full_name,
                    'collections': collections,
                    'phone': volunteer.mobile,
                    'availability': volunteer.availability
                })

            volunteer_location_data.append({
                'name': city,
                'count': volunteer_count,
                'percentage': round((volunteer_count * 100 / total_volunteers) if total_volunteers else 0, 1),
                'top_volunteers': top_volunteers_in_city
            })

    # Top volunteers globally (by collections)
    top_volunteers = []
    volunteer_collections = Inventory.objects.filter(
        collect='yes',
        collected_by_name__isnull=False
    ).values('collected_by_name', 'collected_by_phone').annotate(
        collections=Count('id')
    ).order_by('-collections')[:5]

    for v in volunteer_collections:
        top_volunteers.append({
            'name': v['collected_by_name'],
            'role': 'Volunteer',
            'status': 'active',
            'collections': v['collections'],
            'phone': v['collected_by_phone']
        })

    if not top_volunteers:
        recent_volunteers = Volunteer.objects.order_by('-created_at')[:5]
        for volunteer in recent_volunteers:
            top_volunteers.append({
                'name': volunteer.full_name,
                'role': 'Volunteer',
                'status': 'active',
                'collections': 0,
                'phone': volunteer.mobile
            })

    # Insights (optional AI-style mock insights)
    insights = {
        'peak_day': 'Tuesday',
        'efficiency': round((total_collected * 100 / total_inventory) if total_inventory else 0, 1),
        'engagement': round((volunteers_this_month * 100 / total_volunteers) if total_volunteers else 0, 1),
        'predicted_growth': round(donations_growth * 1.2, 1) if donations_growth > 0 else 15.0
    }

    context = {
        'total_donations': total_donations,
        'total_volunteers': total_volunteers,
        'total_inventory': total_inventory,
        'total_collected': total_collected,
        'total_donors': total_donors,
        'total_notifications': total_notifications,
        'donations_growth': round(abs(donations_growth), 1),
        'volunteers_growth': round(abs(volunteers_growth), 1),
        'monthly_data': json.dumps(monthly_data),
        'donor_location_data': json.dumps(donor_location_data),
        'volunteer_location_data': json.dumps(volunteer_location_data),
        'top_volunteers': json.dumps(top_volunteers),
        'insights': json.dumps(insights),
    }

    return render(request, 'adminpanel/adminAnalytics.html', context)



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
            name = n.volunteer.full_name
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

        # Handle multiple phone numbers separated by commas
        phone_numbers = [phone.strip() for phone in number.split(',') if phone.strip()]
        
        if not phone_numbers:
            messages.error(request, "Please provide at least one phone number.")
            return redirect('send_notification')

        notifications_created = 0
        notifications_failed = 0

        for phone_num in phone_numbers:
            # Create a new Notification object but don't save yet
            notification = Notification(
                number=phone_num,
                gmail=gmail,
                role=role,
                message=message_text,
            )

            # Attach donor or volunteer based on role
            if role == 'donor':
                try:
                    donor = Donor.objects.get(email=gmail, phone=phone_num)
                    notification.donor = donor
                    notification.save()
                    notifications_created += 1
                except Donor.DoesNotExist:
                    # Try to find donor by phone number only
                    try:
                        donor = Donor.objects.get(phone=phone_num)
                        notification.donor = donor
                        notification.gmail = donor.email  # Use the donor's email
                        notification.save()
                        notifications_created += 1
                    except Donor.DoesNotExist:
                        notifications_failed += 1
                        continue

            elif role == 'volunteer':
                try:
                    volunteer = Volunteer.objects.get(email=gmail, mobile=phone_num)
                    notification.volunteer = volunteer
                    notification.save()
                    notifications_created += 1
                except Volunteer.DoesNotExist:
                    # Try to find volunteer by phone number only
                    try:
                        volunteer = Volunteer.objects.get(mobile=phone_num)
                        notification.volunteer = volunteer
                        notification.gmail = volunteer.email  # Use the volunteer's email
                        notification.save()
                        notifications_created += 1
                    except Volunteer.DoesNotExist:
                        notifications_failed += 1
                        continue

        # Provide feedback about the results
        if notifications_created > 0:
            messages.success(request, f"Successfully sent {notifications_created} notification(s).")
        if notifications_failed > 0:
            messages.warning(request, f"Failed to send {notifications_failed} notification(s). User(s) not found.")
        
        return redirect('admin_notifications')

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


def admin_health_analysis(request, volunteer_name):
    """
    Display health analysis results for a specific volunteer
    """
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    from volunteer.models import HealthAnalysis, HealthCheck
    
    try:
        # Get the latest health analysis for this volunteer
        health_analysis = HealthAnalysis.objects.filter(
            volunteer_name=volunteer_name
        ).latest('created_at')
        
        # Get the corresponding health check data
        health_check = HealthCheck.objects.filter(
            volunteer_name=volunteer_name
         ).latest('created_at')
        
        # Parse analysis data
        import json
        analysis_data = json.loads(health_analysis.analysis_data)
        
        context = {
            'health_analysis': health_analysis,
            'health_check': health_check,
            'analysis_data': analysis_data,
            'volunteer_name': volunteer_name
        }
        
        return render(request, 'adminpanel/health_analysis_detail.html', context)
        
    except (HealthAnalysis.DoesNotExist, HealthCheck.DoesNotExist):
        messages.error(request, f"No health data found for volunteer: {volunteer_name}")
        return redirect('admin_volunteers')


def admin_health_decision(request, volunteer_name):
    """
    Handle admin decision (approve/reject) for volunteer health analysis
    """
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    
    if request.method == 'POST':
        decision = request.POST.get('decision')  # 'approved' or 'rejected'
        admin_notes = request.POST.get('admin_notes', '')
        
        from volunteer.models import HealthAnalysis
        from adminpanel.models import Notification
        
        try:
            # Update health analysis with admin decision
            health_analysis = HealthAnalysis.objects.filter(
                volunteer_name=volunteer_name
            ).latest('created_at')
            
            health_analysis.admin_decision = decision
            health_analysis.admin_notes = admin_notes
            health_analysis.save()
            
            # Send notification to volunteer
            if decision == 'approved':
                message = f"Congratulations {health_analysis.volunteer_name}! Your health check has been approved. You are eligible to work with us as a volunteer. Click OK to proceed to login."
                notification_role = 'volunteer_approved'
            else:
                message = f"Dear {health_analysis.volunteer_name}, unfortunately your health check did not meet our requirements. Please register again and retake the health assessment."
                notification_role = 'volunteer_rejected'
            
            # Get volunteer email from the health check
            health_check = HealthCheck.objects.filter(
                volunteer_name=volunteer_name
            ).latest('created_at')
            
            # Create notification
            Notification.objects.create(
                number='',  # Will be filled from volunteer data
                gmail=health_check.volunteer_email,
                role='volunteer',
                message=message
            )
            
            return JsonResponse({
                'success': True,
                'message': f"Decision recorded and notification sent to {health_analysis.volunteer_name}"
            })
            
        except HealthAnalysis.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Health analysis not found'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })
