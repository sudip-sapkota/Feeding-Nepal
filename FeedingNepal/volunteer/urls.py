from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.volunteer_register, name='volunteer_register'),
    path('login/', views.login_view, name='login_view'),
    path('index/', views.index_view, name='volunteer_index'),  # Index page after successful login
    path('foodavailable/', views.food_available, name='food_available'),  # Index page after successful login
    path('accept/', views.accept_view, name='accept_view'),
    path('accept/<int:donation_id>/', views.accept_donation, name='accept_donation'),
    path('donorstracking/', views.donors_tracking, name='donors_tracking'),
    path('send-message/<int:donor_id>/', views.send_message, name='send_message'),
    path('inventory/', views.inventory_view, name='volunteer_inventory'),
    path('inventory/collect/<int:item_id>/', views.collect_inventory, name='collect_inventory'),
    path('donor/<int:donor_id>/report/', views.donor_report, name='donor_report'),
]
