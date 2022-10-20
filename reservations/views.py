from django.utils.http import urlencode
from django.contrib.auth import mixins, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views import generic
from django.forms import formset_factory
from reservations.models import Reservation

from utils.forms import BookByForm, PassengerForm, ReservationInitialForm
from utils.models import Discount, PassengerInfo, Route, Town
from .forms import ReservationForm


class IndexView(generic.TemplateView):
  template_name = 'index.html'
  form = ReservationInitialForm
  

class ReservationInitialView(generic.TemplateView):
  template_name = 'reservation_init_form.html'
  form = ReservationInitialForm

  def get_context_data(self, **kwargs):
    context = super(ReservationInitialView, self).get_context_data(**kwargs)
    context.update({
      "form": self.form,
    })
    return context

  def post(self, request):
    form = self.form(request.POST)  
    data_dict = {}
    if  form.is_valid(): 
      try:
        route = Route.objects.get(origin=form.data['origin'], to=form.data['to']).pk
      except Exception as errors:
        route = None
        print(errors)
        
      if route:
        data_dict.update([ 
          ('route', route),  
          ('book_for', form.data['book_for']),
          ('session', form.data['session']),
          ('d_date', form.data['d_date']),
          ('num_of_passengers', form.data['num_of_passengers'])
        ])
        
        url = '{}?{}'.format(reverse('reservation_form'), urlencode(data_dict))
        return redirect(url)
    
    return render(request, self.template_name, context={
      'form': form,
    })
  

class ReservationView(generic.TemplateView):
  template_name = 'reserve_form.html'
  book_by_form = BookByForm
  
  def data(self):
    route = Route.objects.get(pk=self.request.GET.get('route')) 
    d_date = self.request.GET.get('d_date')
    session = self.request.GET.get('session')
    num_of_passengers = self.request.GET.get('num_of_passengers')
    data = {}
    
    data.update([('route', route), ('session', session),  ('d_date', d_date), ('num_of_passengers', int(num_of_passengers))])
    return data
  
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
    
    if form.is_valid() and formset.is_valid():
      book_by_obj = form.save()
      
      obj = Reservation.objects.create(book_by=book_by_obj, session=data['session'], d_date=data['d_date'])
      
      while forms_count > 0:
        name = formset.data[f"form-{forms_count-1}-name"]
        age = formset.data[f"form-{forms_count-1}-age"]
        contact = formset.data[f"form-{forms_count-1}-contact"]
        gender = formset.data[f"form-{forms_count-1}-gender"]
        
        forms_count -=1
        
        def get_seat():
          last = PassengerInfo.objects.filter(route=data['route']).order_by('seat').last()
          return int(last)+1
        
        p_obj= PassengerInfo.objects.create(name=name, age=age, contact=contact, gender=gender, route=data['route'], seat=get_seat())
        obj.passengers.add(p_obj)
      
      return redirect('book_details', obj.pk)
    
    return render(request, self.template_name, context={
      'book_by_form': form,
      'p_form': formset,
    })
  

class ReservationDetailsView(generic.DetailView):
  template_name = 'book_details.html'
  model = Reservation
  context_object_name = 'book'
 
  def get_context_data(self, **kwargs):
    context = super(ReservationDetailsView, self).get_context_data(**kwargs)
    context.update({
      "p_form": formset_factory(PassengerForm, extra=4),
      "r_form": ReservationForm,
    })
    return context

  def post(self, request):
    pass
  
  
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

  def post(self, request):
    pass
  
  
class AdminReservedView(mixins.LoginRequiredMixin, generic.ListView):
  queryset = Reservation.objects.filter(approved = False)
  template_name = 'reservation.html'
  queryset = Reservation.objects.all()
  context_object_name = 'reserves'

  def get_context_data(self, **kwargs):
    context = super(AdminReservedView, self).get_context_data(**kwargs)
    context.update({
      "towns": Town.objects.all(),
      "discount": Discount.objects.all() 
    })
    return context

  def post(self, request):
    pk = request.POST['pk']
    reserve = request.POST['reserve']
    try:
      disc = Discount.objects.get(pk=request.POST['disc']) 
    except:
      disc = '0'
      
    if pk and pk != '' and disc != '0':
      obj=PassengerInfo.objects.get(pk=pk)
      obj.discount = disc
      obj.save()
      
      r=Reservation.objects.get(pk=reserve)
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