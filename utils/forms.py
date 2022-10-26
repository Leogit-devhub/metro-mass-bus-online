from datetime import datetime
from django import forms
from .models import BookBy, PassengerInfo, Route, Session, Town, UserMessage

class ReservationInitialForm(forms.ModelForm):    
  origin = forms.ModelChoiceField(queryset=Town.objects.all(), label="From", empty_label='')
  to = forms.ModelChoiceField(queryset=Town.objects.all(), empty_label='')
  book_for = forms.ChoiceField(choices=(('', " "), ('self', 'Self'), ('others', 'Others')),)
  d_date = forms.DateField(required=True, label="Departure date", widget=forms.DateInput(attrs={'type':'date', 'min': str(datetime.today().date())}))
  session = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label='')
  num_of_passengers = forms.IntegerField(widget=forms.NumberInput(attrs={'min':'1',}))
  
  def __init__(self, *args, **kwargs):
    super(ReservationInitialForm, self).__init__(*args, **kwargs)
    self.fields["origin"].widget.attrs.update({
      'id':'origin',
      'name':'origin',
      'placeholder': ' ',
      'class': 'btn btn-default form-control'
    })
    
    self.fields["to"].widget.attrs.update({
      'id':'to',
      'name':'to',
      'placeholder': ' ',
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
      'min': '10',
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
  gender = forms.ChoiceField(choices=(('', ""), ('m', 'Male'), ('f', 'Female'), ('o', 'Others')), required=True)
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

    
class UserMessageForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(UserMessageForm, self).__init__(*args, **kwargs)
    self.fields["name"].widget.attrs.update({
      'id':'name',
      'name':'name',
      'type': 'text',
      'class': 'form-control',
    })
    self.fields["phone"].widget.attrs.update({
      'id':'phone',
      'name':'phone',
      'min':'10',
      'class': 'form-control',
    })
    self.fields["email"].widget.attrs.update({
      'id':'email',
      'name':'email',
      'class': 'form-control',
    })
    self.fields["purpose"].widget.attrs.update({
      'id':'purpose',
      'name':'purpose',
      'class': 'form-control',
    })
    self.fields["details"].widget.attrs.update({
      'id':'details',
      'name':'details',
      'class': 'form-control',
    })
  class Meta:
    model = UserMessage
    fields = ("name", "phone", "email", "purpose", "details")
    
