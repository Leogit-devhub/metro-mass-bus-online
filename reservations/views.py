from datetime import datetime, time
from django.utils.http import urlencode
from django.contrib.auth import mixins
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib import messages
from django.forms import formset_factory
from reservations.models import Reservation
from django.contrib.auth.forms import UserCreationForm

from utils.forms import BookByForm, PassengerForm, ReservationInitialForm, UserMessageForm
from utils.models import Buse, PassengerInfo, Route, Session, Town

class CreateUser(generic.CreateView):
  template_name = 'registration/signup.html'
  form_class = UserCreationForm
  success_url = reverse_lazy('reserve')

class IndexView(generic.TemplateView):
  template_name = 'index.html'
  form = UserMessageForm
  
  def get_context_data(self, **kwargs):
    context = super(IndexView, self).get_context_data(**kwargs)
    context.update({
      "form": self.form,
    })
    return context

  def post(self, request, *args, **kwargs):
    form = self.form(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Form Submitted Successfully !')
      return redirect('/')
    
    return render(request, self.template_name, context={
      'form': form,
    })
  
class ReservationInitialView(generic.TemplateView):
  template_name = 'reservation_init_form.html'
  form = ReservationInitialForm

  def get_context_data(self, **kwargs):
    context = super(ReservationInitialView, self).get_context_data(**kwargs)
    context.update({
      "form": self.form,
    })
    return context

  def validation(self, session, date):
    c_date = str(datetime.today().date())
    c_hour = int(datetime.today().time().hour)
    try:
      session = Session.objects.get(pk=session)
    except:
      session = None
    print(session)
    print(session.time.hour)
    print(c_hour)
    if str(date) != c_date:
      return True
    elif session is not None and c_hour <= session.time.hour:
      return True
    return False
    
  def post(self, request):
    form = self.form(request.POST)
    session = form.data['session']
    d_date = form.data['d_date']
    book_for = form.data['book_for']
    validation = self.validation(session=session, date=d_date)
    print(validation)
    data_dict = {}
    if  form.is_valid():  
      origin = form.data['origin']
      to = form.data['to']
      try:
        route = Route.objects.get(origin=origin, to=to).pk
      except Exception as errors:
        origin = Town.objects.get(pk=origin)
        to = Town.objects.get(pk=to)
        route = None
        messages.error(request, f"Seems we have no route for {origin} to {to}. Sorry for that")
        
      if route and validation and book_for !='':
        data_dict.update([ 
          ('route', route),  
          ('book_for', book_for),
          ('session', session),
          ('d_date', d_date),
          ('num_of_passengers', form.data['num_of_passengers'])
        ])
        
        url = '{}?{}'.format(reverse('reservation_form'), urlencode(data_dict))
        return redirect(url)
      
      if not validation:
        messages.error(request, f"Seems you've not selected a session or the session is currently not availabe for the said date!")
      
      if book_for == '':
        messages.error(request, f"Seems you've not selected a 'book for' !")
      
    return render(request, self.template_name, context={
      'form': form,
    })
  

class ReservationView(generic.TemplateView):
  template_name = 'reserve_form.html'
  book_by_form = BookByForm
  
  def data(self):
    route = Route.objects.get(pk=self.request.GET.get('route')) 
    d_date = self.request.GET.get('d_date')
    session = Session.objects.get(pk=self.request.GET.get('session'))
    num_of_passengers = self.request.GET.get('num_of_passengers')
    data = {}
    
    data.update([('route', route), ('session', session),  ('d_date', d_date), ('num_of_passengers', int(num_of_passengers))])
    return data
  
  
  def _bus(self, p_count):
    buses = Buse.objects.filter(route = self.data['route']).order_by('date')
    for bus in buses:
      if bus.bus_full(p_count):
        return bus
    return None   

  def get_context_data(self, **kwargs):
    context = super(ReservationView, self).get_context_data(**kwargs)
    context.update({
      "book_by_form": self.book_by_form,
      "p_form": formset_factory(PassengerForm, extra=self.data()['num_of_passengers']),
    })
    return context

  def post(self, request, *args, **kwargs):
    forms_count = self.data()['num_of_passengers']
    form = self.book_by_form(request.POST)
    formset = formset_factory(PassengerForm, extra=forms_count)(request.POST)
    data = self.data()   
     
    if form.is_valid() and formset.is_valid() and self._bus() is not None:
      book_by_obj = form.save()
      
      obj = Reservation.objects.create(book_by=book_by_obj, bus=self._bus(), session=data['session'], d_date=data['d_date'])
      
      while forms_count > 0:
        name = formset.data[f"form-{forms_count-1}-name"]
        age = formset.data[f"form-{forms_count-1}-age"]
        contact = formset.data[f"form-{forms_count-1}-contact"]
        gender = formset.data[f"form-{forms_count-1}-gender"]
        
        forms_count -=1
        
        def get_seat():
          last = PassengerInfo.objects.filter(route=data['route']).order_by('seat').last()
          if last is not None and last !='':
            return int(last.seat)+1
          return 1
        
        p_obj= PassengerInfo.objects.create(name=name, age=age, contact=contact, gender=gender, route=data['route'], seat=get_seat())
        obj.passengers.add(p_obj)
      
      return redirect('book_details', obj.pk)
    
    messages.error(request, "No Available bus for data['route']). You may call an admin on (024 130 1463)")
    return render(request, self.template_name, context={
      'book_by_form': form,
      'p_form': formset,
    })
  

class ReservationDetailsView(generic.DetailView):
  template_name = 'book_details.html'
  model = Reservation
  context_object_name = 'book'


class ReservationPrintView(generic.DetailView):
  template_name = 'book_print.html'
  model = Reservation
  context_object_name = 'book'
 
  
class AdminTransactionView(mixins.LoginRequiredMixin, generic.ListView):
  queryset = Reservation.objects.filter(approved = True)
  template_name = 'transaction.html'
  queryset = Reservation.objects.all()
  context_object_name = 'reservations'

  def get_context_data(self, **kwargs):
    context = super(AdminTransactionView, self).get_context_data(**kwargs)
    context.update({
      "towns": Town.objects.all(),
    })
    return context
  
  
class AdminReservedView(mixins.LoginRequiredMixin, generic.ListView):
  queryset = Reservation.objects.filter(approved = False)
  template_name = 'reservation.html'
  queryset = Reservation.objects.all()
  context_object_name = 'reserves'

  def get_context_data(self, **kwargs):
    context = super(AdminReservedView, self).get_context_data(**kwargs)
    context.update({
      "towns": Town.objects.all(),
    })
    return context

  def post(self, request):
    r=Reservation.objects.get(pk=request.POST['reserve'])
    r.approved=True
    r.save()
    return redirect('reserve')


class DeletePassenger(generic.DeleteView):
  template_name='utils/modal/confirmation.html'
  model = PassengerInfo
  success_url = reverse_lazy('transaction')

class DeleteReservation(generic.DeleteView):
  template_name='utils/modal/confirmation.html'
  model = Reservation
  success_url = reverse_lazy('reserve')