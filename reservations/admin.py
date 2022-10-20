from django.contrib import admin

from utils.forms import ReservationInitialForm

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
  def get_form(self, request, obj=None, **kwargs):
    return ReservationInitialForm
    
  add_form_template = 'reservation_init_form.html'
  list_display = ("book_by", "passengers_count", "session", "d_date")

