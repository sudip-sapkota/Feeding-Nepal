from django.shortcuts import render, redirect
from django.db import connection
from django.utils import timezone
from .models import Message
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from donor.models import Donor
from django.shortcuts import render, get_object_or_404, redirect
from adminpanel.models import Inventory
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import DonorReport

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

        return redirect('login_view')

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
        item.collect = 'yes'
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