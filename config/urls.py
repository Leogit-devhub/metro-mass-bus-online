from django.contrib import admin
from django.urls import path, include

from reservations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", views.CreateUser.as_view(), name='signup'),
    path('reserved/', views.AdminReservedView.as_view(), name='reserve'),
    path('transaction/', views.AdminTransactionView.as_view(), name='transaction'),
    path('', include('reservations.urls'))
]

admin.site.site_header = "METRO MASS TRANSIT"
admin.site.site_title = "ADMIN DASHBOARD"
admin.site.index_title = "Welcome to Admin Dashboard"
