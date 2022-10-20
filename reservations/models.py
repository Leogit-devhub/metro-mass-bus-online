from django.db import models
from django.urls import reverse

from utils.models import BookBy, PassengerInfo, Route

class Reservation(models.Model):
  Sessions = (
    ('m', 'Morning'),
    ('a', 'Afternoon'),
    ('e', 'Evening'),
  )
  book_by = models.ForeignKey(BookBy, related_name="book_by", on_delete=models.CASCADE, null=True, blank=True)
  passengers = models.ManyToManyField(PassengerInfo, related_name="passenger", null=True, blank=True)
  session = models.CharField(choices=Sessions, max_length=120)
  d_date = models.DateField(max_length=120)
  date_created = models.DateTimeField(auto_now_add = True)
  approved = models.BooleanField(default=False)

  def __str__(self):
    return self.book_by.name

  def passengers_count(self):
    self.passengers.all().count()
    
  def get_absolute_url(self):
    return reverse("book_details", kwargs={"pk": self.pk})

  def get_total_price(self):
    prices = []
    for passenger in self.passengers.all():
      prices.append(passenger.route.price)
    return sum(prices)
  
  def get_route(self):
    return self.passengers.first().route

