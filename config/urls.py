from django.contrib import admin
from django.urls import path, include

from reservations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('reserved/', views.AdminReservedView.as_view(), name='reserve'),
    path('transaction/', views.AdminTransactionView.as_view(), name='transaction'),
    path('', include('reservations.urls'))
]
