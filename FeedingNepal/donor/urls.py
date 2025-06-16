from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='donor_register'),
    path('login/', views.login_view, name='donor_login'),
    path('index/', views.index_view, name='index'),
    path('donation/', views.make_donation, name='make_donation'),  # 🔥 Add this line
    path('donor/', views.search_volunteers, name='search_volunteers'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='donor_register'),
    path('login/', views.login_view, name='donor_login'),
    path('index/', views.index_view, name='index'),
    path('donation/', views.make_donation, name='make_donation'),
    path('donor/', views.search_volunteers, name='search_volunteers'),

    # New menu routes
    
    path('volunteers-tracking/', views.volunteers_tracking_view, name='volunteers_tracking'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('analytic/', views.analytic_view, name='analytic'),
    path('notification/', views.notification_view, name='notification'),
    path('logout/', views.logout_view, name='logout'),
]
