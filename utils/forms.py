from datetime import datetime
from django import forms
from django.contrib import admin

from reservations.models import Reservation

from .models import BookBy, PassengerInfo, Route, Town

class ReservationInitialForm(forms.ModelForm):    
  origin = forms.ModelChoiceField(queryset=Town.objects.all(), label="From")
  to = forms.ModelChoiceField(queryset=Town.objects.all())
  book_for = forms.ChoiceField(choices=(('', "Select your gender"), ('self', 'Self'), ('others', 'Others')),)
  d_date = forms.DateField(required=True, label="Departure date", widget=forms.DateInput(attrs={'type':'date', 'min': str(datetime.today().date())}))
  session = forms.ChoiceField(choices=(('', "Select a session to join"), ('m', 'Morning'), ('a', 'Afternoon'), ('e', 'Evening'),))
  num_of_passengers = forms.IntegerField(widget=forms.NumberInput(attrs={'min':'1',}))
  
  def __init__(self, *args, **kwargs):
    super(ReservationInitialForm, self).__init__(*args, **kwargs)
    self.fields["origin"].widget.attrs.update({
      'id':'origin',
      'name':'origin',
      'class': 'btn btn-default form-control'
    })
    
    self.fields["to"].widget.attrs.update({
      'id':'to',
      'name':'to',
      'class': 'btn btn-default form-control'
    })
    
    self.fields["book_for"].widget.attrs.update({
      'id':'book_for',
      'name':'book_for',
      'class': 'btn btn-default form-control'
    })
    
    self.fields["d_date"].widget.attrs.update({
      'id':'dept-date',
      'name':'d_date',
      'type':'date',
      'class': 'btn btn-default form-control'
    })
    
    self.fields["session"].widget.attrs.update({
      'id':'session',
      'name':'session',
      'class': 'btn btn-default form-control'
    })
    
    self.fields["num_of_passengers"].widget.attrs.update({
      'id':'num_of_passengers',
      'name':'num_of_passengers',
      'class': 'btn btn-default form-control'
    })
  class Meta:
    model = PassengerInfo
    fields = ('origin',)
    

 
class RouteForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(RouteForm, self).__init__(*args, **kwargs)
    self.fields["origin"].widget.attrs.update({
      'id':'origin',
      'name':'origin',
      'type': 'text',
      'class': '',
    })
    self.fields["to"].widget.attrs.update({
      'id':'to',
      'name':'to',
      'class': '',
    })
    self.fields["price"].widget.attrs.update({
      'id':'price',
      'name':'price',
      'class': '',
    })
  class Meta:
    model = Route
    fields = ("origin", "to", "price")  


class BookByForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(BookByForm, self).__init__(*args, **kwargs)
    self.fields["name"].widget.attrs.update({
      'id':'booked_by_name',
      'type':'text',
      'name':'name',
      'class':'form-control'
    })
    self.fields["contact"].widget.attrs.update({
      'id':'booked_by_contact',
      'name':'contact',
      'class':'form-control'
    })
    self.fields["address"].widget.attrs.update({
      'id':'booked_by_address',
      'name':'address',
      'cols':'1',
      'rows':'2',
      'class':'form-control'
    })
    
  class Meta:
    model = BookBy
    fields = ("name", "contact", "address")
    

class PassengerForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(PassengerForm, self).__init__(*args, **kwargs)
    self.fields["name"].widget.attrs.update({
      'id':'name',
      'name':'name',
      'type': 'text',
      'class': 'form-control',
    })
    self.fields["age"].widget.attrs.update({
      'id':'age',
      'name':'age',
      'class': 'form-control',
    })
    self.fields["contact"].widget.attrs.update({
      'id':'contact',
      'name':'contact',
      'min':'10',
      'class': 'form-control',
    })
    self.fields["gender"].widget.attrs.update({
      'id':'gender',
      'name':'gender',
      'class': 'form-control',
    })
  class Meta:
    model = PassengerInfo
    fields = ("name", "age", "contact", "gender")
    


class ReservationInitialAdminForm(admin.ModelAdmin):
  form = ReservationInitialForm