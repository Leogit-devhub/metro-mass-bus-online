from django.contrib import admin

from utils.forms import ReservationInitialForm

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
  list_display = ("book_by", "passengers_count", "session", "d_date", "approved")
