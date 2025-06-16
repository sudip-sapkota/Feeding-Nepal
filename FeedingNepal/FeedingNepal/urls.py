from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Root URL shows index page
    path('donor/', include('donor.urls')),  # This must point to donor/urls.py
    path('volunteer/', include('volunteer.urls')),
    path('adminpanel/', include('adminpanel.urls')),

]
