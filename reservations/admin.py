from django.contrib import admin
from django.contrib.auth.models import User, Group

from utils.forms import ReservationInitialForm

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
  list_display = ("book_by", "passengers_count", "bus", "session", "d_date", "approved")

admin.site.unregister(User)
admin.site.unregister(Group)
