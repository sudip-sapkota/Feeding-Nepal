from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),              # ✅ Django built-in admin
    path('', views.index, name='index'),          # ✅ Home page
    path('donor/', include('donor.urls')),        # ✅ Donor app
    path('volunteer/', include('volunteer.urls')),# ✅ Volunteer app
    path('adminpanel/', include('adminpanel.urls')),  # ✅ Custom admin dashboard
]
