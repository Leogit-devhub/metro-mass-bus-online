from django import forms
from django.contrib import admin

from .models import Reservation


class ReservationForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(ReservationForm, self).__init__(*args, **kwargs)
    self.fields["book_by"].widget.attrs.update({
      'id':'book_by',
      'name':'book_by',
      'class':''
    })
    self.fields["passengers"].widget.attrs.update({
      'id':'passengers',
      'name':'passengers',
      'class':''
    })
    self.fields["session"].widget.attrs.update({
      'id':'session',
      'name':'session',
      'class':''
    })
    self.fields["d_date"].widget.attrs.update({
      'id':'d_date',
      'name':'d_date',
      'class':''
    })
  class Meta:
    model = Reservation
    fields = ("book_by", "passengers", "session", "d_date")
    