from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('index/', views.admin_index, name='admin_index'),

    # Sidebar routes
    path('donors/', views.admin_donors, name='admin_donors'),
    path('volunteers/', views.admin_volunteers, name='admin_volunteers'),
    path('donations/', views.admin_donations, name='admin_donations'),
    
    path('apply-food/', views.admin_apply_food, name='admin_apply_food'),
    path('analytics/', views.admin_analytics, name='admin_analytics'),
    path('reports/', views.admin_reports, name='admin_reports'),
    path('notifications/', views.admin_notifications, name='admin_notifications'),
    path('settings/', views.admin_settings, name='admin_settings'),
    path('inventory/', views.admin_inventory, name='admin_inventory'),
    path('add/', views.add_data, name='add_data'),
    path('update-inventory/', views.update_inventory, name='update_inventory'),
    path('notifications/send/', views.send_notification_page, name='send_notification'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    
    path('delete_donation/<int:id>/', views.delete_item, name='delete_item'), 
    path('delete_donor/<int:id>/', views.delete_item_donor, name='delete_item_donor'),
    path('edit_inventory/<int:id>/', views.edit_inventory, name='edit_inventory'),
    path('delete_inventory/<int:id>/', views.delete_inventory, name='delete_inventory'),
    path('edit_notification/<int:id>/', views.edit_notification, name='edit_notification'),
    path('delete_notification/<int:id>/', views.delete_notification, name='delete_notification'),
] 
